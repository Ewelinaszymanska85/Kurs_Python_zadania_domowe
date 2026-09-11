import asyncio
import json
import socket

import redis.asyncio as redis
from aiohttp import web, WSMsgType


CHANNEL_NAME = "chat_messages"


async def websocket_handler(request: web.Request) -> web.WebSocketResponse:
    """Obsługuje połączenie WebSocket pojedynczego użytkownika."""
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    app = request.app
    app["websockets"].add(ws)

    hostname = socket.gethostname()

    try:
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                data = json.loads(msg.data)
                message_text = data.get("message", "")

                payload = json.dumps({
                    "message": message_text,
                    "served_by": hostname,
                })

                await app["redis"].publish(CHANNEL_NAME, payload)

            elif msg.type == WSMsgType.ERROR:
                print(f"[ERROR] Polaczenie WebSocket zamkniete z bledem: {ws.exception()}")

    finally:
        app["websockets"].discard(ws)

    return ws


async def redis_listener(app: web.Application) -> None:
    """Nasłuchuje na kanale Redis Pub/Sub i przekazuje wiadomości do wszystkich WebSocketów tej instancji."""
    pubsub = app["redis"].pubsub()
    await pubsub.subscribe(CHANNEL_NAME)

    async for message in pubsub.listen():
        if message["type"] != "message":
            continue

        for ws in set(app["websockets"]):
            if not ws.closed:
                await ws.send_str(message["data"])


async def start_background_tasks(app: web.Application) -> None:
    app["websockets"] = set()
    app["redis"] = redis.Redis(host="redis", port=6379, decode_responses=True)
    app["redis_listener_task"] = asyncio.create_task(redis_listener(app))


async def cleanup_background_tasks(app: web.Application) -> None:
    app["redis_listener_task"].cancel()
    await app["redis"].close()


def create_app() -> web.Application:
    app = web.Application()
    app.router.add_get("/ws", websocket_handler)
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)
    return app


if __name__ == "__main__":
    web.run_app(create_app(), host="0.0.0.0", port=8000)