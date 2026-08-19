"""
CRUD API: Dodawanie produktu.
Tworzy produkt na podstawie danych JSON i zapisuje go w bazie SQLite.
"""
from aiohttp import web
from sqlalchemy import String
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column
)


DATABASE_URL = "sqlite+aiosqlite:///products.db"


class Base(DeclarativeBase):
    pass


class Product(Base):
    """Model produktu."""

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[int]


engine = create_async_engine(DATABASE_URL)
Session = async_sessionmaker(engine)


async def create_product(request):
    """Tworzy nowy produkt."""

    dane = await request.json()

    product = Product(
        name=dane["name"],
        price=dane["price"]
    )

    async with Session() as session:
        session.add(product)
        await session.commit()
        await session.refresh(product)

    return web.json_response({
        "id": product.id,
        "name": product.name,
        "price": product.price
    }, status=201)


async def create_app():
    """Tworzy aplikację i bazę danych."""

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    app = web.Application()

    app.router.add_post(
        "/products",
        create_product
    )

    return app


if __name__ == "__main__":
    web.run_app(
        create_app(),
        port=8080
    )