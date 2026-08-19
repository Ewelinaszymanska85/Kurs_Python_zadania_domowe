from flask import Flask

app = Flask(__name__)


@app.route("/me")
def me():
    """Endpoint /me - strona "O mnie"."""
    imie = "Ewelina"
    nazwisko = "Kowalska"
    return f"{imie} {nazwisko}"


@app.route("/add/<int:num1>/<int:num2>")
def add(num1, num2):
    """
    Endpoint /add/<num1>/<num2> - prosty kalkulator sumujący dwie liczby.

    Fragmenty <int:num1> i <int:num2> w ścieżce to tzw. "zmienne trasy"
    (route variables) - Flask automatycznie wyodrębnia te wartości
    z adresu URL i przekazuje je jako argumenty do funkcji.

    Konwerter "int:" mówi Flaskowi, żeby:
    1. Zaakceptował w tym miejscu URL-a TYLKO liczby całkowite
       (jeśli ktoś wpisze np. /add/abc/5, Flask zwróci błąd 404,
       bo "abc" nie jest liczbą całkowitą)
    2. Automatycznie skonwertował tekst z URL-a na typ int w Pythonie
       (bez konwertera, num1 i num2 byłyby zwykłymi stringami)

    Przykład wywołania: /add/5/3 -> "Wynik to: 8"
    """
    suma = num1 + num2
    return f"Wynik to: {suma}"


if __name__ == "__main__":
    app.run(debug=True) 