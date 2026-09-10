import psutil
from aiohttp import web


async def health_check(request: web.Request) -> web.Response:
    """Endpoint /health - zwraca status aplikacji i użycie pamięci."""
    memory = psutil.virtual_memory()

    status_data = {
        "status": "ok",
        "memory": {
            "total_mb": round(memory.total / (1024 ** 2), 1),
            "used_mb": round(memory.used / (1024 ** 2), 1),
            "available_mb": round(memory.available / (1024 ** 2), 1),
            "percent_used": memory.percent,
        },
    }

    # Jeśli pamięć jest krytycznie zapełniona, zgłoś to statusem 503.
    if memory.percent >= 95.0:
        status_data["status"] = "degraded"
        return web.json_response(status_data, status=503)

    return web.json_response(status_data, status=200)


def create_app() -> web.Application:
    """Tworzy aplikację Aiohttp z zarejestrowanym endpointem /health."""
    app = web.Application()
    app.router.add_get("/health", health_check)
    return app


if __name__ == "__main__":
    web.run_app(create_app(), host="localhost", port=8080)