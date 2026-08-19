import time
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.orm import joinedload
from dotenv import load_dotenv
import os

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


class Room(db.Model):
    __tablename__ = "rooms"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Reservation(db.Model):
    __tablename__ = "reservations"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"), nullable=False)

    user = db.relationship("User")
    room = db.relationship("Room")


# =========================
# INIT DB - dane testowe
# =========================

def db_init():
    with app.app_context():
        db.create_all()

        if not User.query.first():
            users = [User(name=f"Użytkownik {i}") for i in range(1, 6)]
            rooms = [Room(name=f"Sala {i}") for i in range(1, 4)]
            db.session.add_all(users + rooms)
            db.session.commit()

            reservations = []
            for i in range(1, 21):
                reservations.append(Reservation(
                    title=f"Rezerwacja {i}",
                    user_id=users[i % len(users)].id,
                    room_id=rooms[i % len(rooms)].id,
                ))
            db.session.add_all(reservations)
            db.session.commit()


# =========================
# DEBUGGING: Licznik zapytań SQL
# =========================
query_count = 0

with app.app_context():
    db_init()

    @event.listens_for(db.engine, "before_cursor_execute")
    def count_queries(conn, cursor, statement, parameters, context, executemany):
        global query_count
        query_count += 1


@app.route("/debug/n-plus-1")
def debug_n_plus_1():
    """
    Porównanie problemu N+1 (bez optymalizacji) z wersją z joinedload.
    Dla każdej rezerwacji pobiera: tytuł, nazwę sali, imię użytkownika.
    """
    global query_count

    # ❌ ZŁY SPOSÓB - Problem N+1
    query_count = 0
    start = time.time()

    reservations = Reservation.query.all()    # Zapytanie 1
    bad_result = []
    for r in reservations:
        # Każde r.user i r.room wywołuje NOWE zapytanie!
        bad_result.append({
            "tytul": r.title,
            "sala": r.room.name,
            "uzytkownik": r.user.name,
        })

    bad_time = time.time() - start
    bad_queries = query_count

    # ✅ DOBRY SPOSÓB - Eager Loading (joinedload)
    query_count = 0
    start = time.time()

    reservations = Reservation.query.options(
        joinedload(Reservation.user),   # Dołącz użytkownika od razu
        joinedload(Reservation.room),   # Dołącz salę od razu
    ).all()  # Jedno zapytanie z JOIN

    good_result = []
    for r in reservations:
        # Tutaj NIE MA nowych zapytań - dane są już w pamięci
        good_result.append({
            "tytul": r.title,
            "sala": r.room.name,
            "uzytkownik": r.user.name,
        })

    good_time = time.time() - start
    good_queries = query_count

    return jsonify({
        "bez_optymalizacji": {
            "liczba_zapytan_sql": bad_queries,
            "czas_ms": round(bad_time * 1000, 2),
            "wyniki": bad_result,
        },
        "z_optymalizacja_joinedload": {
            "liczba_zapytan_sql": good_queries,
            "czas_ms": round(good_time * 1000, 2),
            "wyniki": good_result,
        },
        "roznica": f"{bad_queries / good_queries:.0f}x mniej zapytań" if good_queries else "n/a",
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
    app.run(debug=True) 