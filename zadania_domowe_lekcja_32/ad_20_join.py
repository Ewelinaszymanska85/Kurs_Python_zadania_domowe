"""
SQLAlchemy Async JOIN.
Pobiera produkt razem z nazwą użytkownika,
który go utworzył.
"""
from aiohttp import web
from sqlalchemy import (
    select,
    String,
    ForeignKey
)
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column
)


DATABASE_URL = "sqlite+aiosqlite:///shop.db"


class Base(DeclarativeBase):
    pass


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100)
    )


class Product(Base):

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100)
    )

    price: Mapped[int]

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )


engine = create_async_engine(DATABASE_URL)
Session = async_sessionmaker(engine)


async def get_product(request):
    """Pobiera produkt wraz z nazwą jego autora."""

    product_id = int(
        request.match_info["id"]
    )

    async with Session() as session:

        result = await session.execute(
            select(Product, User)
            .join(User)
            .where(Product.id == product_id)
        )

        wynik = result.first()

    if wynik is None:
        raise web.HTTPNotFound(
            text="Produkt nie istnieje"
        )

    product, user = wynik

    return web.json_response({
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "created_by": user.name
    })


async def create_app():

    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all
        )

    app = web.Application()

    app.router.add_get(
        "/products/{id}",
        get_product
    )

    return app


if __name__ == "__main__":
    web.run_app(
        create_app(),
        port=8080
    )