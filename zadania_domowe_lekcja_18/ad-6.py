from flask import Flask, request, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
import random
import io
import calendar

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Flowable
)

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# =========================
# MODELE (niezależne od poprzednich zadań)
# =========================

class ReportRoom(db.Model):
    """Sala z ceną za godzinę wynajmu - potrzebną do liczenia przychodu."""
    __tablename__ = "report_rooms"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price_per_hour = db.Column(db.Numeric(10, 2), nullable=False)


class ReportUser(db.Model):
    __tablename__ = "report_users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class ReportReservation(db.Model):
    """Rezerwacja używana wyłącznie do generowania raportów miesięcznych."""
    __tablename__ = "report_reservations"

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey("report_rooms.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("report_users.id"), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    room = db.relationship("ReportRoom")
    user = db.relationship("ReportUser")


# =========================
# DANE TESTOWE
# =========================

def seed_report_data():
    """Tworzy tabele i wypełnia je danymi testowymi z ostatnich 2 miesięcy."""
    db.create_all()

    if ReportRoom.query.first():
        return

    rooms = [
        ReportRoom(name=f"Sala {i}", price_per_hour=random.choice([50, 80, 100, 150, 200]))
        for i in range(1, 9)
    ]
    users = [ReportUser(name=f"Użytkownik {i}") for i in range(1, 16)]
    db.session.add_all(rooms + users)
    db.session.commit()

    reservations = []
    teraz = datetime.now()

    for i in range(400):
        dni_wstecz = random.randint(0, 59)
        data = teraz - timedelta(days=dni_wstecz)
        godzina = random.choice(range(8, 18))
        start = data.replace(hour=godzina, minute=0, second=0, microsecond=0)
        czas_trwania_h = random.choice([1, 2, 3])
        end = start + timedelta(hours=czas_trwania_h)

        reservations.append(ReportReservation(
            room_id=random.choice(rooms).id,
            user_id=random.choice(users).id,
            start_time=start,
            end_time=end,
        ))

    db.session.add_all(reservations)
    db.session.commit()


# =========================
# LOGIKA RAPORTU
# =========================

def get_month_range(month_str: str):
    """Zamienia string "2024-01" na (pierwszy_dzien, ostatni_dzien_miesiaca)."""
    rok, miesiac = map(int, month_str.split("-"))
    _, ostatni_dzien = calendar.monthrange(rok, miesiac)

    start = datetime(rok, miesiac, 1, 0, 0, 0)
    end = datetime(rok, miesiac, ostatni_dzien, 23, 59, 59)
    return start, end


class SimpleBarChart(Flowable):
    """
    Prosty wykres słupkowy rysowany NATYWNIE wewnątrz PDF, bez konwersji
    do obrazu rastrowego (PNG). Dziedziczy po Flowable, więc reportlab
    traktuje go jak każdy inny element dokumentu (Paragraph, Table itd.)
    i sam zajmuje się jego umieszczeniem na stronie.

    To podejście NIE wymaga żadnych zewnętrznych bibliotek graficznych
    (matplotlib, cairo, freetype) - rysuje słupki jako proste prostokąty
    używając wyłącznie wbudowanego mechanizmu canvas reportlab.
    """

    def __init__(self, data: dict, width=460, height=180):
        super().__init__()
        self.data = data
        self.width = width
        self.height = height

    def draw(self):
        canv = self.canv
        dni = sorted(self.data.keys())
        wartosci = [self.data[d] for d in dni]
        max_wartosc = max(wartosci) if wartosci else 1

        obszar_wykresu_h = self.height - 30  # miejsce na etykiety osi X
        szerokosc_slupka = self.width / max(len(dni), 1) * 0.7
        odstep = self.width / max(len(dni), 1)

        canv.setFont("Helvetica", 6)

        for i, dzien in enumerate(dni):
            wartosc = self.data[dzien]
            wysokosc_slupka = (wartosc / max_wartosc) * obszar_wykresu_h
            x = i * odstep
            y = 20  # podnosimy słupki, żeby było miejsce na etykiety pod nimi

            canv.setFillColor(colors.HexColor("#4568dc"))
            canv.rect(x, y, szerokosc_slupka, wysokosc_slupka, fill=1, stroke=0)

            # Etykieta dnia miesiąca pod słupkiem
            canv.setFillColor(colors.black)
            canv.drawCentredString(x + szerokosc_slupka / 2, 8, str(dzien))

            # Wartość nad słupkiem
            canv.drawCentredString(x + szerokosc_slupka / 2, y + wysokosc_slupka + 3, str(wartosc))


# =========================
# ENDPOINT - RAPORT MIESIĘCZNY (PDF)
# =========================

@app.route("/api/reports/monthly")
def monthly_report():
    """
    Generuje raport PDF dla podanego miesiąca.
    Przykład wywołania: /api/reports/monthly?month=2026-06

    Raport zawiera:
    1. Podsumowanie: liczba rezerwacji, łączny czas (h), przychód (zł)
    2. Tabelę: top 10 sal (po liczbie rezerwacji)
    3. Tabelę: top 10 użytkowników (po liczbie rezerwacji)
    4. Wykres: liczba rezerwacji dziennie w danym miesiącu
    """
    month_str = request.args.get("month")
    if not month_str:
        return {"error": "Parametr 'month' jest wymagany, np. ?month=2026-06"}, 400

    try:
        start, end = get_month_range(month_str)
    except ValueError:
        return {"error": "Niepoprawny format. Użyj: YYYY-MM, np. 2026-06"}, 400

    rezerwacje = (
        ReportReservation.query
        .filter(ReportReservation.start_time >= start, ReportReservation.start_time <= end)
        .all()
    )

    if not rezerwacje:
        return {"error": f"Brak rezerwacji w miesiącu {month_str}"}, 404

    # --- 1. PODSUMOWANIE ---
    liczba_rezerwacji = len(rezerwacje)
    laczny_czas_h = sum(
        (r.end_time - r.start_time).total_seconds() / 3600 for r in rezerwacje
    )
    przychod = sum(
        float(r.room.price_per_hour) * ((r.end_time - r.start_time).total_seconds() / 3600)
        for r in rezerwacje
    )

    # --- 2. TOP 10 SAL ---
    sale_licznik = {}
    for r in rezerwacje:
        sale_licznik[r.room.name] = sale_licznik.get(r.room.name, 0) + 1
    top_sale = sorted(sale_licznik.items(), key=lambda x: x[1], reverse=True)[:10]

    # --- 3. TOP 10 UŻYTKOWNIKÓW ---
    uzytkownicy_licznik = {}
    for r in rezerwacje:
        uzytkownicy_licznik[r.user.name] = uzytkownicy_licznik.get(r.user.name, 0) + 1
    top_uzytkownicy = sorted(uzytkownicy_licznik.items(), key=lambda x: x[1], reverse=True)[:10]

    # --- 4. WYKRES - rezerwacje per dzień miesiąca ---
    rezerwacje_per_dzien = {}
    for r in rezerwacje:
        dzien = r.start_time.day
        rezerwacje_per_dzien[dzien] = rezerwacje_per_dzien.get(dzien, 0) + 1

    # =========================
    # BUDOWA PDF (reportlab)
    # =========================
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=A4,
                             topMargin=2 * cm, bottomMargin=2 * cm)
    styles = getSampleStyleSheet()
    story = []

    tytul_style = ParagraphStyle(
        "TytulRaportu", parent=styles["Title"], fontSize=20, spaceAfter=20
    )

    story.append(Paragraph(f"Raport miesięczny - {month_str}", tytul_style))
    story.append(Spacer(1, 12))

    # --- Sekcja: podsumowanie ---
    story.append(Paragraph("Podsumowanie", styles["Heading2"]))
    podsumowanie_data = [
        ["Liczba rezerwacji", str(liczba_rezerwacji)],
        ["Łączny czas wynajmu (h)", f"{laczny_czas_h:.1f}"],
        ["Przychód (zł)", f"{przychod:,.2f}"],
    ]
    podsumowanie_table = Table(podsumowanie_data, colWidths=[8 * cm, 6 * cm])
    podsumowanie_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#4568dc")),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(podsumowanie_table)
    story.append(Spacer(1, 20))

    # --- Sekcja: top 10 sal ---
    story.append(Paragraph("Top 10 sal (liczba rezerwacji)", styles["Heading2"]))
    sale_data = [["Sala", "Liczba rezerwacji"]] + [[nazwa, str(ile)] for nazwa, ile in top_sale]
    sale_table = Table(sale_data, colWidths=[8 * cm, 6 * cm])
    sale_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#11998e")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f0f0")]),
    ]))
    story.append(sale_table)
    story.append(Spacer(1, 20))

    # --- Sekcja: top 10 użytkowników ---
    story.append(Paragraph("Top 10 użytkowników (liczba rezerwacji)", styles["Heading2"]))
    user_data = [["Użytkownik", "Liczba rezerwacji"]] + [[nazwa, str(ile)] for nazwa, ile in top_uzytkownicy]
    user_table = Table(user_data, colWidths=[8 * cm, 6 * cm])
    user_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#fc4a1a")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f0f0")]),
    ]))
    story.append(user_table)
    story.append(Spacer(1, 20))

    # --- Sekcja: wykres (rysowany natywnie w PDF, bez PNG) ---
    story.append(Paragraph("Wykres wykorzystania (rezerwacje dziennie)", styles["Heading2"]))
    story.append(Spacer(1, 10))
    story.append(SimpleBarChart(rezerwacje_per_dzien, width=460, height=180))

    doc.build(story)
    pdf_buffer.seek(0)

    return send_file(
        pdf_buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"raport_{month_str}.pdf",
    )


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
        seed_report_data()
    app.run(debug=True) 