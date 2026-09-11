import os

from aiohttp import web
import asyncpg


async def get_db_pool(app: web.Application) -> None:
    app["db_pool"] = await asyncpg.create_pool(
        host=os.environ["DB_HOST"],
        port=os.environ.get("DB_PORT", "5432"),
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )

    yield

    await app["db_pool"].close()


async def list_items(request: web.Request) -> web.Response:
    pool = request.app["db_pool"]

    async with pool.acquire() as connection:
        rows = await connection.fetch("SELECT id, name FROM items ORDER BY id")

    return web.json_response([dict(row) for row in rows])


async def list_admins(request: web.Request) -> web.Response:
    pool = request.app["db_pool"]

    async with pool.acquire() as connection:
        rows = await connection.fetch("SELECT id, username FROM admins ORDER BY id")

    return web.json_response([dict(row) for row in rows])


def create_app() -> web.Application:
    app = web.Application()
    app.cleanup_ctx.append(get_db_pool)
    app.router.add_get("/items", list_items)
    app.router.add_get("/admins", list_admins)
    return app


if __name__ == "__main__":
    web.run_app(create_app(), host="0.0.0.0", port=8000)