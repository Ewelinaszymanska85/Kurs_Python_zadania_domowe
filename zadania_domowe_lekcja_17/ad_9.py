from flask import Flask, render_template
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
    """Model produktu - identyczny jak w zadaniu 8, bo korzystamy
    z tej samej tabeli "products" w bazie danych."""
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Product {self.name} - {self.price} zł>"


@app.route("/products")
def products():
    """
    Endpoint /products - wyświetla wszystkie produkty z bazy danych
    w formie tabeli HTML.

    Product.query.all() wykonuje zapytanie SQL (SELECT * FROM products)
    i zwraca listę obiektów Product - każdy reprezentuje jeden wiersz
    z tabeli. Przekazujemy tę listę do szablonu, gdzie iterujemy
    przez nią, wyświetlając każdy produkt jako wiersz <tr> w tabeli.
    """
    wszystkie_produkty = Product.query.all()
    return render_template("products.html", products=wszystkie_produkty)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    