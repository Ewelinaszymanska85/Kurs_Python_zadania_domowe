from flask import Flask

app = Flask(__name__)


@app.route("/me")
def me():
    """
    Endpoint zwracający podstawowe dane o autorze aplikacji.
    Najprostszy przykład trasy (route) w Flasku - funkcja zwraca
    string, który automatycznie staje się treścią odpowiedzi HTTP.
    """
    return "Ewelina Szymańska"  # <- wpisz tutaj swoje imię i nazwisko


if __name__ == "__main__":
    app.run(debug=True) 