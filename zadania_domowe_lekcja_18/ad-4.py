from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, event
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
import random

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# =========================
# MODELE
# =========================

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(50), nullable=False)

    # Flaga oznaczająca admina - admin dostaje powiadomienia
    # o każdej nowej rezerwacji w systemie
    is_admin = db.Column(db.Boolean, default=False)


class Room(db.Model):
    __tablename__ = "rooms"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Reservation(db.Model):
    __tablename__ = "reservations"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"), nullable=False)

    # Flaga pomocnicza - zapobiega wysłaniu tego samego przypomnienia
    # "za 1h" więcej niż raz dla tej samej rezerwacji
    reminder_sent = db.Column(db.Boolean, default=False)

    user = db.relationship("User")
    room = db.relationship("Room")


class Notification(db.Model):
    """
    Powiadomienie dla użytkownika. Dwa scenariusze tworzenia:
    1. Automatycznie, gdy ktoś utworzy nową rezerwację (powiadomienie
       trafia do admina) - obsługuje to event listener after_insert.
    2. Automatycznie, gdy do startu rezerwacji zostaje ok. 1h
       (przypomnienie dla użytkownika) - obsługuje to funkcja
       check_upcoming_reservations(), uruchamiana okresowo.
    """
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    user = db.relationship("User")


# =========================
# AUTOMATYCZNE POWIADOMIENIA
# =========================

@event.listens_for(Reservation, "after_insert")
def create_notification_for_admin(mapper, connection, reservation):
    """
    Event listener SQLAlchemy - odpala się automatycznie PO zapisaniu
    nowej rezerwacji do bazy (after_insert). Tworzy powiadomienie
    dla admina informujące o nowej rezerwacji.

    Uwaga: w evencie after_insert używamy connection.execute() z surowym
    INSERT-em, a nie db.session.add()/commit() - bo jesteśmy w trakcie
    "flush" sesji i normalny ORM-owy zapis mógłby spowodować błędy
    rekurencji/synchronizacji stanu sesji.
    """
    admin = User.query.filter_by(is_admin=True).first()

    if admin:
        connection.execute(
            Notification.__table__.insert().values(
                user_id=admin.id,
                message=f"Nowa rezerwacja: {reservation.title}",
                is_read=False,
                created_at=datetime.utcnow(),
            )
        )


def check_upcoming_reservations():
    """
    Sprawdza, czy są rezerwacje zaczynające się w ciągu najbliższej
    godziny, dla których jeszcze nie wysłano przypomnienia.
    Dla każdej takiej rezerwacji tworzy powiadomienie dla użytkownika
    i oznacza ją jako "przypomnienie wysłane" (reminder_sent = True),
    żeby nie wysyłać tego samego przypomnienia wielokrotnie.

    W realnej aplikacji ta funkcja byłaby wywoływana okresowo przez
    scheduler (np. APScheduler albo cron) - tutaj wywołujemy ją
    manualnie / przy starcie, żeby zademonstrować logikę.
    """
    teraz = datetime.now()  
    za_godzine = teraz + timedelta(hours=1)

    nadchodzace = Reservation.query.filter(
        Reservation.start_time >= teraz,
        Reservation.start_time <= za_godzine,
        Reservation.reminder_sent == False,
    ).all()

    for rezerwacja in nadchodzace:
        notification = Notification(
            user_id=rezerwacja.user_id,
            message=f"Przypomnienie: rezerwacja '{rezerwacja.title}' "
                     f"zaczyna się o {rezerwacja.start_time.strftime('%H:%M')}",
        )
        db.session.add(notification)
        rezerwacja.reminder_sent = True

    if nadchodzace:
        db.session.commit()

    return len(nadchodzace)


# =========================
# INIT DB - dane testowe
# =========================

def db_init(): 
    db.create_all()

    if User.query.first():
        return

    departamenty = ["IT", "Marketing", "Sprzedaż", "HR", "Finanse"]

    users = [
        User(name=f"Użytkownik {i}", department=random.choice(departamenty))
        for i in range(1, 21)
    ]
    # Pierwszy użytkownik jest adminem - do niego trafiają powiadomienia
    # o nowych rezerwacjach
    users[0].is_admin = True
    users[0].name = "Admin"

    rooms = [Room(name=f"Sala {i}") for i in range(1, 5)]
    db.session.add_all(users + rooms)
    db.session.commit()

    godziny_pracy = list(range(8, 18))
    reservations = []
    teraz = datetime.now()

    for i in range(300):
        dni_wstecz = random.randint(0, 29)
        losowa_data = teraz - timedelta(days=dni_wstecz)

        if random.random() < 0.7:
            godzina = random.choice([10, 11, 12, 13, 14, 15])
        else:
            godzina = random.choice(godziny_pracy)

        start_time = losowa_data.replace(
            hour=godzina, minute=random.choice([0, 15, 30, 45]),
            second=0, microsecond=0
        )

        reservations.append(Reservation(
            title=f"Rezerwacja {i + 1}",
            start_time=start_time,
            user_id=random.choice(users).id,
            room_id=random.choice(rooms).id,
        ))

    # Dodatkowa rezerwacja zaczynająca się za 30 minut - do testowania
    # przypomnienia "za 1h" bez czekania na prawdziwy czas
    reservations.append(Reservation(
        title="Spotkanie testowe (wkrótce)",
        start_time=teraz + timedelta(minutes=30),
        user_id=users[1].id,
        room_id=rooms[0].id,
    ))

    db.session.add_all(reservations)
    db.session.commit()


# =========================
# ENDPOINTY - POWIADOMIENIA
# =========================

@app.route("/api/notifications")
def get_notifications():
    """Zwraca listę nieprzeczytanych powiadomień, najnowsze pierwsze."""
    notifications = (
        Notification.query
        .filter_by(is_read=False)
        .order_by(Notification.created_at.desc())
        .all()
    )

    return jsonify([
        {
            "id": n.id,
            "user_id": n.user_id,
            "message": n.message,
            "created_at": str(n.created_at),
            "is_read": n.is_read,
        }
        for n in notifications
    ])


@app.route("/api/notifications/<int:id>/read", methods=["POST"])
def mark_notification_read(id):
    """Oznacza konkretne powiadomienie jako przeczytane."""
    notification = Notification.query.get_or_404(id)
    notification.is_read = True
    db.session.commit()

    return jsonify({
        "status": "ok",
        "message": "Powiadomienie oznaczone jako przeczytane",
    })


@app.route("/api/notifications/check-upcoming", methods=["POST"])
def trigger_upcoming_check():
    """
    Endpoint pomocniczy do RĘCZNEGO wywołania sprawdzenia nadchodzących
    rezerwacji (symuluje to, co normalnie robiłby scheduler co minutę).
    Przydatne do testowania zadania 4 bez czekania na prawdziwy czas.
    """
    ile_utworzono = check_upcoming_reservations()
    return jsonify({
        "status": "ok",
        "nowe_przypomnienia": ile_utworzono,
    })


@app.route("/test-db")
def test_db():
    try:
        from sqlalchemy import text
        db.session.execute(text("SELECT 1"))
        return "Połączenie OK!"
    except Exception as e:
        return f"Błąd połączenia z bazą: {e}"


if __name__ == "__main__":
    with app.app_context():
        db_init()
    app.run(debug=True) 