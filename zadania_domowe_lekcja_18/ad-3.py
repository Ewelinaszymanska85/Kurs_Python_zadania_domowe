from flask import Flask, jsonify, render_template 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
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
    # Departament, do którego przypisany jest użytkownik
    # (np. "IT", "Marketing", "Sprzedaż") - używany do wykresu kołowego
    department = db.Column(db.String(50), nullable=False)


class Room(db.Model):
    __tablename__ = "rooms"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Reservation(db.Model):
    __tablename__ = "reservations"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)

    # Data i godzina rezerwacji - kluczowe dla heatmapy i trendu
    start_time = db.Column(db.DateTime, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"), nullable=False)

    user = db.relationship("User")
    room = db.relationship("Room")


# =========================
# INIT DB - dane testowe
# =========================

def db_init():
    """
    Tworzy tabele i wypełnia bazę realistycznymi danymi testowymi:
    - użytkownicy przypisani do różnych departamentów
    - rezerwacje rozłożone na różne dni tygodnia, godziny i daty
      z ostatnich 30 dni (żeby heatmapa i trend miały sens)
    """
    db.create_all()

    if User.query.first():
        return 

    departamenty = ["IT", "Marketing", "Sprzedaż", "HR", "Finanse"]

    users = [
        User(name=f"Użytkownik {i}", department=random.choice(departamenty))
        for i in range(1, 21)
    ]
    rooms = [Room(name=f"Sala {i}") for i in range(1, 5)]
    db.session.add_all(users + rooms)
    db.session.commit()

    # Godziny pracy biura - rezerwacje są bardziej prawdopodobne
    # w godzinach 8-17, żeby heatmapa miała realistyczny wzorzec
    godziny_pracy = list(range(8, 18))

    reservations = []
    teraz = datetime.now()

    for i in range(300):
        # Losowy dzień z ostatnich 30 dni
        dni_wstecz = random.randint(0, 29)
        losowa_data = teraz - timedelta(days=dni_wstecz)

        # Losowa godzina, z przewagą godzin pracy (10-16) - symulacja
        # realistycznego wzorca, w którym południe jest popularniejsze
        if random.random() < 0.7:
            godzina = random.choice([10, 11, 12, 13, 14, 15])
        else:
            godzina = random.choice(godziny_pracy)

        start_time = losowa_data.replace(
            hour=godzina, minute=random.choice([0, 15, 30, 45]),
            second=0, microsecond=0
        )

        reservations.append(Reservation(
            title=f"Rezerwacja {i+1}",
            start_time=start_time,
            user_id=random.choice(users).id,
            room_id=random.choice(rooms).id,
        ))

    db.session.add_all(reservations)
    db.session.commit()


# =========================
# ENDPOINT - ROZSZERZONE STATYSTYKI
# =========================

@app.route("/dashboard/extended-stats")
def extended_stats():
    """
    Zwraca trzy zestawy danych statystycznych do rozbudowy dashboardu:

    1. pie_chart_departments - liczba rezerwacji per departament
       (do wykresu kołowego)
    2. heatmap_day_hour - macierz dzień tygodnia x godzina, pokazująca
       które kombinacje są najpopularniejsze
    3. trend_last_30_days - liczba rezerwacji dziennie w ostatnich 30 dniach
    """

    # -----------------------------------------------------------------
    # 1. WYKRES KOŁOWY - rezerwacje per departament
    # -----------------------------------------------------------------
    # Łączymy Reservation z User, żeby dotrzeć do pola department,
    # grupujemy po departamencie i liczymy rezerwacje w każdej grupie
    departament_query = (
        db.session.query(
            User.department,
            func.count(Reservation.id).label("liczba_rezerwacji")
        )
        .join(Reservation, Reservation.user_id == User.id)
        .group_by(User.department)
        .all()
    )

    pie_chart_departments = [
        {"departament": dep, "liczba_rezerwacji": count}
        for dep, count in departament_query
    ]

    # -----------------------------------------------------------------
    # 2. HEATMAPA - dzień tygodnia x godzina
    # -----------------------------------------------------------------
    # func.extract('dow', ...) wyciąga dzień tygodnia z daty:
    # w PostgreSQL 0 = niedziela, 1 = poniedziałek, ..., 6 = sobota
    # func.extract('hour', ...) wyciąga samą godzinę (0-23)
    heatmap_query = (
        db.session.query(
            func.extract("dow", Reservation.start_time).label("dzien_tygodnia"),
            func.extract("hour", Reservation.start_time).label("godzina"),
            func.count(Reservation.id).label("liczba_rezerwacji")
        )
        .group_by("dzien_tygodnia", "godzina")
        .all()
    )

    # Mapujemy numer dnia tygodnia (0-6) na czytelną nazwę po polsku
    nazwy_dni = ["Niedziela", "Poniedziałek", "Wtorek", "Środa",
                 "Czwartek", "Piątek", "Sobota"]

    heatmap_day_hour = [
        {
            "dzien_tygodnia": nazwy_dni[int(dzien)],
            "godzina": int(godzina),
            "liczba_rezerwacji": count,
        }
        for dzien, godzina, count in heatmap_query
    ]

    # -----------------------------------------------------------------
    # 3. TREND - liczba rezerwacji dziennie w ostatnich 30 dniach
    # -----------------------------------------------------------------
    # Grupujemy po samej dacie (bez godziny), pomijając rezerwacje
    # starsze niż 30 dni
    trzydziesc_dni_temu = datetime.now() - timedelta(days=30)

    trend_query = (
        db.session.query(
            func.date(Reservation.start_time).label("data"),
            func.count(Reservation.id).label("liczba_rezerwacji")
        )
        .filter(Reservation.start_time >= trzydziesc_dni_temu)
        .group_by(func.date(Reservation.start_time))
        .order_by(func.date(Reservation.start_time))
        .all()
    )

    trend_last_30_days = [
        {"data": str(data), "liczba_rezerwacji": count}
        for data, count in trend_query
    ]

    return jsonify({
        "pie_chart_departments": pie_chart_departments,
        "heatmap_day_hour": heatmap_day_hour,
        "trend_last_30_days": trend_last_30_days,
    }) 
    

@app.route("/dashboard")
def dashboard(): 
    return render_template("dashboard.html") 


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