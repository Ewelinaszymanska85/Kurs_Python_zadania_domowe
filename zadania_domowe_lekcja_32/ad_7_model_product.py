"""
SQLAlchemy Async: Definicja modelu.
Tworzy model Product z ID, nazwą i ceną.
"""
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String


class Base(DeclarativeBase):
    pass


class Product(Base):
    """Model produktu."""

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100)
    )

    price: Mapped[int]