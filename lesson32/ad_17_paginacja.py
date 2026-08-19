"""
Paginacja produktów.
Pobiera produkty stronami za pomocą parametrów page i limit.
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


async def get_products(request):
    """Zwraca określoną stronę produktów."""

    page = int(request.query.get("page", 1))
    limit = int(request.query.get("limit", 10))

    if page < 1 or limit < 1:
        raise web.HTTPBadRequest(
            text="page i limit muszą być większe od 0"
        )

    offset = (page - 1) * limit

    async with Session() as session:

        result = await session.execute(
            select(Product)
            .offset(offset)
            .limit(limit)
        )

        produkty = result.scalars().all()

    return web.json_response({
        "page": page,
        "limit": limit,
        "products": [
            {
                "id": product.id,
                "name": product.name,
                "price": product.price
            }
            for product in produkty
        ]
    })


async def create_app():

    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all
        )

    app = web.Application()

    app.router.add_get(
        "/products",
        get_products
    )

    return app


if __name__ == "__main__":
    web.run_app(
        create_app(),
        port=8080
    )