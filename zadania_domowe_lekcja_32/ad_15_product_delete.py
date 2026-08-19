"""
CRUD API: Usuwanie produktu.
Usuwa produkt z bazy danych i zwraca HTTP 204.
"""
from aiohttp import web
from sqlalchemy import select, String
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

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[int]


engine = create_async_engine(DATABASE_URL)
Session = async_sessionmaker(engine)


async def delete_product(request):
    """Usuwa produkt po ID."""

    product_id = int(
        request.match_info["id"]
    )

    async with Session() as session:

        result = await session.execute(
            select(Product).where(
                Product.id == product_id
            )
        )

        product = result.scalar_one_or_none()

        if product is None:
            raise web.HTTPNotFound(
                text="Produkt nie istnieje"
            )

        await session.delete(product)
        await session.commit()

    return web.Response(status=204)


async def create_app():

    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all
        )

    app = web.Application()

    app.router.add_delete(
        "/products/{id}",
        delete_product
    )

    return app


if __name__ == "__main__":
    web.run_app(
        create_app(),
        port=8080
    )