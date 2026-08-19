"""
SQLAlchemy Async: Transakcja.
Przelew środków pomiędzy dwoma kontami.
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


DATABASE_URL = "sqlite+aiosqlite:///bank.db"


class Base(DeclarativeBase):
    pass


class Account(Base):

    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)

    balance: Mapped[int] = mapped_column(
        default=0
    )


engine = create_async_engine(DATABASE_URL)
Session = async_sessionmaker(engine)


async def transfer(request):
    """Wykonuje przelew pomiędzy dwoma kontami."""

    dane = await request.json()

    from_id = dane["from_id"]
    to_id = dane["to_id"]
    amount = dane["amount"]

    async with Session() as session:

        async with session.begin():

            result = await session.execute(
                select(Account).where(
                    Account.id.in_([from_id, to_id])
                )
            )

            konta = {
                konto.id: konto
                for konto in result.scalars()
            }

            if from_id not in konta or to_id not in konta:
                raise web.HTTPNotFound(
                    text="Nie znaleziono konta"
                )

            konto_nadawcy = konta[from_id]
            konto_odbiorcy = konta[to_id]

            if konto_nadawcy.balance < amount:
                raise web.HTTPBadRequest(
                    text="Brak wystarczających środków"
                )

            konto_nadawcy.balance -= amount
            konto_odbiorcy.balance += amount

    return web.json_response({
        "status": "OK",
        "from_id": from_id,
        "to_id": to_id,
        "amount": amount
    })


async def create_app():

    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all
        )

    app = web.Application()

    app.router.add_post(
        "/transfer",
        transfer
    )

    return app


if __name__ == "__main__":
    web.run_app(
        create_app(),
        port=8080
    ) 