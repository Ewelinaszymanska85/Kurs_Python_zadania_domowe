import os
import time

from aiohttp import web
import asyncpg
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST


REQUEST_COUNT = Counter(
    "http_requests_total", "Liczba requestow HTTP", ["method", "endpoint", "status"]
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds", "Czas trwania requestu HTTP", ["endpoint"]
)


@web.middleware
async def metrics_middleware(request: web.Request, handler):
    """Middleware zbierające metryki dla każdego requestu."""
    start_time = time.time()

    try:
        response = await handler(request)
        status = response.status
    except web.HTTPException as exc:
        status = exc.status
        raise
    finally:
        duration = time.time() - start_time
        REQUEST_LATENCY.labels(endpoint=request.path).observe(duration)
        REQUEST_COUNT.labels(
            method=request.method, endpoint=request.path, status=status,
        ).inc()

    return response


async def get_db_pool(app: web.Application) -> None:
    app["db_pool"] = await asyncpg.create_pool(
        host=os.environ["DB_HOST"],
        port=os.environ.get("DB_PORT", "5432"),
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )

    async with app["db_pool"].acquire() as connection:
        await connection.execute(
            "CREATE TABLE IF NOT EXISTS books (id SERIAL PRIMARY KEY, title TEXT NOT NULL, author TEXT NOT NULL)"
        )

    yield

    await app["db_pool"].close()


async def list_books(request: web.Request) -> web.Response:
    pool = request.app["db_pool"]

    async with pool.acquire() as connection:
        rows = await connection.fetch("SELECT id, title, author FROM books ORDER BY id")

    return web.json_response([dict(row) for row in rows])


async def create_book(request: web.Request) -> web.Response:
    data = await request.json()
    title = data.get("title")
    author = data.get("author")

    if not title or not author:
        return web.json_response({"error": "Wymagane pola: title, author"}, status=400)

    pool = request.app["db_pool"]

    async with pool.acquire() as connection:
        row = await connection.fetchrow(
            "INSERT INTO books (title, author) VALUES ($1, $2) RETURNING id, title, author",
            title, author,
        )

    return web.json_response(dict(row), status=201)


async def metrics_endpoint(request: web.Request) -> web.Response:
    """Endpoint /metrics eksponujący dane w formacie Prometheus."""
    return web.Response(body=generate_latest(), content_type=CONTENT_TYPE_LATEST)


def create_app() -> web.Application:
    app = web.Application(middlewares=[metrics_middleware])

    app.cleanup_ctx.append(get_db_pool)

    app.router.add_get("/books", list_books)
    app.router.add_post("/books", create_book)
    app.router.add_get("/metrics", metrics_endpoint)

    return app


if __name__ == "__main__":
    web.run_app(create_app(), host="0.0.0.0", port=8000)