"""
Mock API dla AI.
Symuluje długie przetwarzanie zapytania przez AI.
"""
from aiohttp import web
import asyncio


async def chat(request):
    """Symuluje przetwarzanie promptu przez AI."""

    dane = await request.json()

    prompt = dane.get("prompt")

    if not prompt:
        raise web.HTTPBadRequest(
            text="Brak parametru prompt"
        )

    # Symulacja długiego przetwarzania AI
    await asyncio.sleep(3)

    return web.json_response({
        "response": (
            f"Otrzymałem twój prompt: "
            f"'{prompt}' i przetworzyłem go."
        )
    })


def create_app():

    app = web.Application()

    app.router.add_post(
        "/api/v1/chat",
        chat
    )

    return app


if __name__ == "__main__":
    web.run_app(
        create_app(),
        port=8080
    )