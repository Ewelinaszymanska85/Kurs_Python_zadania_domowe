import os

from aiohttp import web
import asyncpg


async def setup_database(app: web.Application) -> None:
    """Tworzy pulę połączeń i tabelę users przy starcie."""
    app["db_pool"] = await asyncpg.create_pool(
        host=os.environ["DB_HOST"],
        port=os.environ.get("DB_PORT", "5432"),
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )

    async with app["db_pool"].acquire() as connection:
        await connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL
            )
            """
        )

        count = await connection.fetchval("SELECT COUNT(*) FROM users")

        if count == 0:
            await connection.execute(
                "INSERT INTO users (name, email) VALUES ($1, $2), ($3, $4)",
                "Anna Kowalska", "anna@example.com",
                "Piotr Nowak", "piotr@example.com",
            )

    yield

    await app["db_pool"].close()


async def get_user(request: web.Request) -> web.Response:
    user_id = int(request.match_info["user_id"])
    pool = request.app["db_pool"]

    async with pool.acquire() as connection:
        row = await connection.fetchrow(
            "SELECT id, name, email FROM users WHERE id = $1", user_id,
        )

    if row is None:
        return web.json_response({"error": "Uzytkownik nie znaleziony"}, status=404)

    return web.json_response(dict(row))


async def list_users(request: web.Request) -> web.Response:
    pool = request.app["db_pool"]

    async with pool.acquire() as connection:
        rows = await connection.fetch("SELECT id, name, email FROM users ORDER BY id")

    return web.json_response([dict(row) for row in rows])


def create_app() -> web.Application:
    app = web.Application()
    app.cleanup_ctx.append(setup_database)
    app.router.add_get("/users", list_users)
    app.router.add_get("/users/{user_id}", get_user)
    return app


if __name__ == "__main__":
    web.run_app(create_app(), host="0.0.0.0", port=8001)