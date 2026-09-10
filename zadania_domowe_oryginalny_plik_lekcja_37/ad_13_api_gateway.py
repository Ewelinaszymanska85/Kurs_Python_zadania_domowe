import aiohttp
from aiohttp import web


USERS_SERVICE_URL = "http://users-service:8001"
POSTS_SERVICE_URL = "http://posts-service:8002"


async def get_user_with_posts(request: web.Request) -> web.Response:
    """Agreguje dane użytkownika i jego postów z dwóch osobnych serwisów."""
    user_id = request.match_info["user_id"]

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{USERS_SERVICE_URL}/users/{user_id}") as user_response:
            if user_response.status == 404:
                return web.json_response({"error": "Uzytkownik nie znaleziony"}, status=404)
            user_data = await user_response.json()

        async with session.get(f"{POSTS_SERVICE_URL}/posts/user/{user_id}") as posts_response:
            posts_data = await posts_response.json()

    return web.json_response({
        "user": user_data,
        "posts": posts_data,
        "posts_count": len(posts_data),
    })


async def list_all_users(request: web.Request) -> web.Response:
    """Proxy do users-service."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{USERS_SERVICE_URL}/users") as response:
            data = await response.json()

    return web.json_response(data)


def create_app() -> web.Application:
    app = web.Application()
    app.router.add_get("/users", list_all_users)
    app.router.add_get("/users/{user_id}/full", get_user_with_posts)
    return app


if __name__ == "__main__":
    web.run_app(create_app(), host="0.0.0.0", port=8000)