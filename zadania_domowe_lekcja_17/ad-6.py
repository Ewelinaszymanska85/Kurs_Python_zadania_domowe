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


@app.route("/book")
def book():
    """
    Endpoint /book - wyświetla informacje o książce, przekazane
    jako słownik do szablonu book.html.

    W Pythonie słownik (dict) to struktura par klucz-wartość, np.
    ksiazka['title'] zwróci "Hobbit". W szablonie Jinja2 odwołujemy
    się do pól słownika podobnie - przez {{ book.title }} albo
    {{ book['title'] }} (obie składnie działają identycznie).
    """
    ksiazka = {
        "title": "Hobbit",
        "author": "J.R.R. Tolkien",
        "year": 1937,
    }

    return render_template("book.html", book=ksiazka)


if __name__ == "__main__":
    app.run(debug=True) 