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


@app.route("/gallery")
def gallery():
    """
    Endpoint /gallery - wyświetla prostą galerię obrazków.

    Każdy element listy "obrazki" to słownik z dwoma kluczami:
    - url: link do obrazka w internecie (np. z Picsum - serwisu
      z darmowymi obrazkami testowymi)
    - caption: podpis pod obrazkiem

    W szablonie iterujemy przez tę listę, wyświetlając każdy obrazek
    (<img>) z odpowiadającym mu podpisem (<p>).
    """
    obrazki = [
        {
            "url": "https://picsum.photos/seed/gory/400/300",
            "caption": "Widok na góry",
        },
        {
            "url": "https://picsum.photos/seed/morze/400/300",
            "caption": "Zachód słońca nad morzem",
        },
        {
            "url": "https://picsum.photos/seed/las/400/300",
            "caption": "Spacer po lesie",
        },
        {
            "url": "https://picsum.photos/seed/miasto/400/300",
            "caption": "Nocne miasto",
        },
    ]

    return render_template("gallery.html", images=obrazki)


if __name__ == "__main__":
    app.run(debug=True) 