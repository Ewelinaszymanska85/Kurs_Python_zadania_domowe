from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from datetime import datetime, timedelta
from dateutil.rrule import rrule, WEEKLY
import os
import uuid

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# =========================
# MODEL
# =========================

class Booking(db.Model):
    """
    Pojedyncze wystąpienie rezerwacji (może być częścią serii cyklicznej
    albo rezerwacją jednorazową - wtedy series_id i recurrence_rule
    są None).
    """
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)

    room_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    # Reguła powtarzania - np. "WEEKLY", "BIWEEKLY". None dla
    # rezerwacji jednorazowych (nie będących częścią serii).
    recurrence_rule = db.Column(db.String(20), nullable=True)

    # UUID łączący wszystkie wystąpienia tej samej serii cyklicznej.
    # Przechowywany jako string (36 znaków - standardowy zapis UUID).
    series_id = db.Column(db.String(36), nullable=True, index=True)

    # Flaga pozwalająca "miękko" usunąć (anulować) rezerwację bez
    # fizycznego wykasowania jej z bazy - przydatne do zachowania
    # historii i statystyk
    is_cancelled = db.Column(db.Boolean, default=False)


# =========================
# LOGIKA GENEROWANIA SERII
# =========================

# Mapa reguł powtarzania na interwał w tygodniach (dla rrule WEEKLY,
# interval=1 oznacza co tydzień, interval=2 oznacza co dwa tygodnie)
RECURRENCE_INTERVALS = {
    "WEEKLY": 1,
    "BIWEEKLY": 2,
}


def generate_occurrences(start_time: datetime, recurrence_rule: str, until: datetime):
    """
    Generuje listę dat startowych dla wszystkich wystąpień serii,
    używając biblioteki python-dateutil (rrule).

    WEEKLY -> co 7 dni
    BIWEEKLY -> co 14 dni
    (interval w rrule mnoży się przez bazową częstotliwość WEEKLY)
    """
    if recurrence_rule not in RECURRENCE_INTERVALS:
        raise ValueError(
            f"Nieznana reguła powtarzania: {recurrence_rule}. "
            f"Dostępne: {list(RECURRENCE_INTERVALS.keys())}"
        )

    interval = RECURRENCE_INTERVALS[recurrence_rule]

    daty = list(rrule(
        freq=WEEKLY,
        interval=interval,
        dtstart=start_time,
        until=until,
    ))

    return daty


def find_conflicts(room_id: int, start_time: datetime, end_time: datetime,
                    exclude_booking_id: int = None):
    """
    Sprawdza, czy istnieje już aktywna (nieanulowana) rezerwacja tej
    samej sali, która nakłada się w czasie z podanym przedziałem
    [start_time, end_time].

    Dwa przedziały czasowe nakładają się, gdy:
        nowy_start < istniejacy_end  ORAZ  nowy_end > istniejacy_start
    """
    query = Booking.query.filter(
        Booking.room_id == room_id,
        Booking.is_cancelled == False,
        Booking.start_time < end_time,
        Booking.end_time > start_time,
    )

    if exclude_booking_id is not None:
        query = query.filter(Booking.id != exclude_booking_id)

    return query.all()


# =========================
# ENDPOINT - TWORZENIE SERII REZERWACJI
# =========================

@app.route("/api/bookings/series", methods=["POST"])
def create_booking_series():
    """
    Tworzy serię cyklicznych rezerwacji na podstawie "wzorca" i reguły
    powtarzania.

    Oczekiwany JSON:
    {
        "title": "Spotkanie zespołu",
        "room_id": 1,
        "user_id": 2,
        "start_time": "2026-07-01T10:00:00",
        "duration_minutes": 60,
        "recurrence_rule": "WEEKLY",
        "until": "2026-09-30T00:00:00"
    }

    Strategia walidacji: sprawdzamy konflikty dla WSZYSTKICH wystąpień
    PRZED zapisaniem czegokolwiek do bazy. Jeśli choć jedno wystąpienie
    koliduje z istniejącą rezerwacją, odrzucamy całą serię (nie tworzymy
    "dziurawej" serii z brakującymi terminami) i zwracamy listę
    konfliktów, żeby użytkownik mógł zmienić termin.
    """
    data = request.get_json()

    try:
        title = data["title"]
        room_id = data["room_id"]
        user_id = data["user_id"]
        start_time = datetime.fromisoformat(data["start_time"])
        duration_minutes = data["duration_minutes"]
        recurrence_rule = data["recurrence_rule"]
        until = datetime.fromisoformat(data["until"])
    except (KeyError, ValueError) as e:
        return jsonify({"error": f"Niepoprawne lub brakujące dane: {e}"}), 400

    try:
        daty_wystapien = generate_occurrences(start_time, recurrence_rule, until)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    if not daty_wystapien:
        return jsonify({"error": "Reguła powtarzania nie wygenerowała żadnych wystąpień"}), 400

    czas_trwania = timedelta(minutes=duration_minutes)

    # --- KROK 1: sprawdzamy konflikty dla WSZYSTKICH wystąpień ---
    konflikty = []
    for data_startu in daty_wystapien:
        data_konca = data_startu + czas_trwania
        kolidujace = find_conflicts(room_id, data_startu, data_konca)

        if kolidujace:
            konflikty.append({
                "proponowany_start": data_startu.isoformat(),
                "proponowany_koniec": data_konca.isoformat(),
                "koliduje_z": [
                    {"id": k.id, "title": k.title, "start_time": k.start_time.isoformat()}
                    for k in kolidujace
                ],
            })

    if konflikty:
        return jsonify({
            "status": "konflikt",
            "message": "Nie utworzono serii - wykryto konflikty w niektórych terminach",
            "konflikty": konflikty,
        }), 409  # 409 Conflict

    # --- KROK 2: brak konfliktów - tworzymy całą serię ---
    series_id = str(uuid.uuid4())
    nowe_rezerwacje = []

    for data_startu in daty_wystapien:
        booking = Booking(
            title=title,
            room_id=room_id,
            user_id=user_id,
            start_time=data_startu,
            end_time=data_startu + czas_trwania,
            recurrence_rule=recurrence_rule,
            series_id=series_id,
        )
        db.session.add(booking)
        nowe_rezerwacje.append(booking)

    db.session.commit()

    return jsonify({
        "status": "ok",
        "series_id": series_id,
        "liczba_utworzonych_rezerwacji": len(nowe_rezerwacje),
        "rezerwacje": [
            {
                "id": b.id,
                "start_time": b.start_time.isoformat(),
                "end_time": b.end_time.isoformat(),
            }
            for b in nowe_rezerwacje
        ],
    }), 201  # 201 Created


# =========================
# ENDPOINT - ANULOWANIE
# =========================

@app.route("/api/bookings/<int:booking_id>/cancel", methods=["POST"])
def cancel_single_booking(booking_id):
    """Anuluje TYLKO jedno, konkretne wystąpienie rezerwacji."""
    booking = Booking.query.get_or_404(booking_id)
    booking.is_cancelled = True
    db.session.commit()

    return jsonify({
        "status": "ok",
        "message": f"Rezerwacja {booking_id} została anulowana",
    })


@app.route("/api/bookings/series/<string:series_id>/cancel", methods=["POST"])
def cancel_series(series_id):
    """
    Anuluje WSZYSTKIE wystąpienia należące do danej serii.
    Domyślnie anuluje też przeszłe wystąpienia - jeśli chcemy anulować
    tylko przyszłe, można dodać filtr Booking.start_time >= datetime.now().
    """
    bookings = Booking.query.filter_by(series_id=series_id, is_cancelled=False).all()

    if not bookings:
        return jsonify({"error": "Nie znaleziono aktywnych rezerwacji dla tej serii"}), 404

    for booking in bookings:
        booking.is_cancelled = True

    db.session.commit()

    return jsonify({
        "status": "ok",
        "message": f"Anulowano całą serię {series_id}",
        "liczba_anulowanych": len(bookings),
    })


# =========================
# ENDPOINT POMOCNICZY - PODGLĄD REZERWACJI
# =========================

@app.route("/api/bookings")
def list_bookings():
    """Lista wszystkich aktywnych (nieanulowanych) rezerwacji - do podglądu/testów."""
    bookings = Booking.query.filter_by(is_cancelled=False).order_by(Booking.start_time).all()

    return jsonify([
        {
            "id": b.id,
            "title": b.title,
            "room_id": b.room_id,
            "user_id": b.user_id,
            "start_time": b.start_time.isoformat(),
            "end_time": b.end_time.isoformat(),
            "recurrence_rule": b.recurrence_rule,
            "series_id": b.series_id,
        }
        for b in bookings
    ])


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
        db.create_all()
    app.run(debug=True) 