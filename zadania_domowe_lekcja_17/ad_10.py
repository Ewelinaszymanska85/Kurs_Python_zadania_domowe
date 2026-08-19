from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Registration(db.Model):
    """
    Model zgłoszenia/rejestracji na wydarzenie.

    - name: imię osoby rejestrującej się
    - email: adres email, unique=True oznacza, że baza danych
      NIE POZWOLI zapisać dwóch rejestracji z tym samym adresem
      email - próba dodania duplikatu zakończy się błędem na
      poziomie bazy danych (integrity error)
    """
    __tablename__ = "registrations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"<Registration {self.name} ({self.email})>"


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Endpoint /register - obsługuje DWA różne typy żądań HTTP
    pod tym samym adresem URL:

    GET  -> użytkownik dopiero WCHODZI na stronę - po prostu
            wyświetlamy mu formularz (pusty, do wypełnienia)

    POST -> użytkownik WYSŁAŁ już wypełniony formularz - musimy:
            1. odebrać dane z formularza (request.form)
            2. stworzyć nowy obiekt Registration
            3. zapisać go w bazie danych
            4. przekierować użytkownika na stronę z podziękowaniem
               (PRG pattern - Post/Redirect/Get - zapobiega to
               przypadkowemu ponownemu wysłaniu formularza, gdyby
               użytkownik odświeżył stronę po rejestracji)

    request.method pozwala sprawdzić, jakim typem żądania przyszło
    dane wywołanie - dzięki temu jedna funkcja może obsłużyć
    obie sytuacje.
    """
    if request.method == "POST":
        # request.form to słownik-podobny obiekt zawierający dane
        # wysłane przez formularz HTML metodą POST. Kluczami są
        # wartości atrybutu "name" z poszczególnych pól <input>
        imie = request.form["name"]
        email = request.form["email"]

        nowa_rejestracja = Registration(name=imie, email=email)
        db.session.add(nowa_rejestracja)
        db.session.commit()

        # Przekierowanie (redirect) wysyła do przeglądarki odpowiedź
        # HTTP 302, mówiącą "przejdź na inny adres" - tutaj na stronę
        # podziękowania. url_for("thank_you") generuje adres URL na
        # podstawie NAZWY funkcji (a nie wpisanej na sztywno ścieżki),
        # co jest bezpieczniejsze przy zmianach struktury aplikacji.
        return redirect(url_for("thank_you"))

    # Jeśli żądanie jest typu GET (czyli ktoś po prostu otworzył
    # stronę), wyświetlamy formularz do wypełnienia
    return render_template("register.html")


@app.route("/thank-you")
def thank_you():
    """Prosta strona z podziękowaniem, wyświetlana po udanej rejestracji."""
    return "<h1>Dziękujemy za rejestrację! 🎉</h1>"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True) 