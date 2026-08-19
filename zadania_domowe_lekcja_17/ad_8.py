from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Product(db.Model):
    """
    Model SQLAlchemy reprezentujący produkt w bazie danych.

    - id: klucz główny (primary_key=True), automatycznie generowany
      przez bazę danych jako liczba całkowita, unikalna dla każdego
      wiersza w tabeli
    - name: nazwa produktu, typ String, nullable=False oznacza,
      że to pole NIE MOŻE być puste (NULL) - baza odrzuci próbę
      zapisania produktu bez nazwy
    - price: cena produktu, typ Float, również nullable=False
    """
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        """
        Reprezentacja tekstowa obiektu Product - przydatna podczas
        pracy w interaktywnej konsoli Pythona, bo dzięki niej
        print(produkt) albo samo wpisanie "produkt" w konsoli
        pokaże czytelny opis, a nie coś w stylu <Product object at 0x...>
        """
        return f"<Product {self.name} - {self.price} zł>"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True) 