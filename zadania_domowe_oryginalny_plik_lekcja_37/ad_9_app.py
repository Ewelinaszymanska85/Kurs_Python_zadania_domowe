import asyncio
import json
import time

import redis.asyncio as redis
from aiohttp import web


CACHE_TTL_SECONDS = 30


async def fetch_from_fake_database(item_id: str) -> dict:
    """Symuluje wolne zapytanie do bazy danych (np. 2 sekundy)."""
    await asyncio.sleep(2)

    return {
        "id": item_id,
        "name": f"Item {item_id}",
        "generated_at": time.time(),
    }


async def get_item(request: web.Request) -> web.Response:
    """Endpoint zwracający dane z cache lub, jeśli brak, z 'bazy danych'."""
    item_id = request.match_info["item_id"]
    redis_client: redis.Redis = request.app["redis"]

    cache_key = f"item:{item_id}"
    cached_value = await redis_client.get(cache_key)

    if cached_value is not None:
        data = json.loads(cached_value)
        data["source"] = "cache"
        return web.json_response(data)

    data = await fetch_from_fake_database(item_id)
    data["source"] = "database"

    await redis_client.set(cache_key, json.dumps(data), ex=CACHE_TTL_SECONDS)

    return web.json_response(data)


async def create_app() -> web.Application:
    app = web.Application()

    app["redis"] = redis.Redis(host="redis", port=6379, decode_responses=True)

    app.router.add_get("/items/{item_id}", get_item)

    return app


if __name__ == "__main__":
    web.run_app(create_app(), host="0.0.0.0", port=8000)