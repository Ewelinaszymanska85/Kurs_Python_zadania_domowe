from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Wczytujemy zmienne środowiskowe z pliku .env (SECRET_KEY, DATABASE_URL, FLASK_ENV)
load_dotenv()

app = Flask(__name__)

# Konfiguracja Flask - SECRET_KEY potrzebny m.in. do sesji i ciasteczek
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Connection string do bazy PostgreSQL, odczytany z .env
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

# Wyłączamy śledzenie modyfikacji obiektów (niepotrzebne, zużywa pamięć,
# SQLAlchemy i tak ostrzega o tym przy starcie, jeśli nie ustawimy False)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicjalizacja obiektu SQLAlchemy powiązanego z naszą aplikacją Flask
db = SQLAlchemy(app)


@app.route("/test-db")
def test_db():
    """
    Endpoint testowy - sprawdza, czy aplikacja faktycznie łączy się
    z bazą danych PostgreSQL. Wykonuje proste zapytanie SQL (SELECT 1),
    które nie wymaga istnienia żadnej tabeli - służy tylko do weryfikacji
    samego połączenia.
    """
    try:
        # db.session.execute() pozwala wykonać "surowe" zapytanie SQL
        # text("SELECT 1") to najprostsze możliwe zapytanie testowe
        from sqlalchemy import text
        db.session.execute(text("SELECT 1"))
        return "Połączenie OK!"
    except Exception as e:
        # Jeśli coś pójdzie nie tak (np. złe hasło, baza nie istnieje),
        # zwracamy komunikat błędu, żeby łatwo zdiagnozować problem
        return f"Błąd połączenia z bazą: {e}"


if __name__ == "__main__":
    app.run(debug=True) 