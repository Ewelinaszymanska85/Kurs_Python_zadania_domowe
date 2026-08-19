from flask import Flask, render_template

app = Flask(__name__)


@app.route("/me")
def me():
    """Endpoint /me - strona "O mnie"."""
    imie = "Ewelina"
    nazwisko = "Kowalska"
    return f"{imie} {nazwisko}"


@app.route("/add/<int:num1>/<int:num2>")
def add(num1, num2):
    """Endpoint /add/<num1>/<num2> - prosty kalkulator."""
    suma = num1 + num2
    return f"Wynik to: {suma}"


@app.route("/movies")
def movies():
    """
    Endpoint /movies - wyświetla listę ulubionych filmów z dynamicznym
    tytułem strony (page_title), przekazanym do dedykowanego szablonu
    movies_ad4.html.
    """
    lista_filmow = [
        "Incepcja",
        "Pulp Fiction",
        "Matrix",
        "Skazani na Shawshank",
        "Władca Pierścieni: Powrót Króla",
    ]

    tytul_strony = "Moje ulubione filmy"

    return render_template(
        "movies_ad4.html",
        movies=lista_filmow,
        page_title=tytul_strony,
    )


if __name__ == "__main__":
    app.run(debug=True) 