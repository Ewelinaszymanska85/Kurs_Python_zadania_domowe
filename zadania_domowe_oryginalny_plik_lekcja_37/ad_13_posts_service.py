import os

from aiohttp import web
import asyncpg


async def setup_database(app: web.Application) -> None:
    """Tworzy pulę połączeń i tabelę posts przy starcie."""
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
            CREATE TABLE IF NOT EXISTS posts (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL
            )
            """
        )

        count = await connection.fetchval("SELECT COUNT(*) FROM posts")

        if count == 0:
            await connection.execute(
                """
                INSERT INTO posts (user_id, title, content) VALUES
                (1, 'Pierwszy post', 'Tresc pierwszego postu'),
                (1, 'Drugi post', 'Tresc drugiego postu'),
                (2, 'Post Piotra', 'Tresc postu Piotra')
                """
            )

    yield

    await app["db_pool"].close()


async def list_posts(request: web.Request) -> web.Response:
    pool = request.app["db_pool"]

    async with pool.acquire() as connection:
        rows = await connection.fetch("SELECT id, user_id, title, content FROM posts ORDER BY id")

    return web.json_response([dict(row) for row in rows])


async def get_posts_by_user(request: web.Request) -> web.Response:
    user_id = int(request.match_info["user_id"])
    pool = request.app["db_pool"]

    async with pool.acquire() as connection:
        rows = await connection.fetch(
            "SELECT id, user_id, title, content FROM posts WHERE user_id = $1 ORDER BY id",
            user_id,
        )

    return web.json_response([dict(row) for row in rows])


def create_app() -> web.Application:
    app = web.Application()
    app.cleanup_ctx.append(setup_database)
    app.router.add_get("/posts", list_posts)
    app.router.add_get("/posts/user/{user_id}", get_posts_by_user)
    return app


if __name__ == "__main__":
    web.run_app(create_app(), host="0.0.0.0", port=8002)