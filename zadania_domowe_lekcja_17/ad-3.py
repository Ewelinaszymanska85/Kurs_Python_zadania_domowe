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
    Endpoint /movies - wyświetla listę ulubionych filmów.

    Używa dedykowanego szablonu movies_ad3.html (osobnego dla tego
    zadania), żeby kolejne zadania (4, 5...) mogły rozbudowywać
    swoje własne, niezależne wersje szablonu bez wpływu na ten plik.
    """
    lista_filmow = [
        "Incepcja",
        "Pulp Fiction",
        "Matrix",
        "Skazani na Shawshank",
        "Władca Pierścieni: Powrót Króla",
    ]

    return render_template("movies_ad3.html", movies=lista_filmow)


if __name__ == "__main__":
    app.run(debug=True) 