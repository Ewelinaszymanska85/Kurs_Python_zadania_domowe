import asyncio

from aiohttp.test_utils import TestClient, TestServer

from ad_17_app import create_app


async def _test_handle_returns_200():
    app = create_app()
    server = TestServer(app)
    client = TestClient(server)

    await client.start_server()

    response = await client.get("/")
    assert response.status == 200

    text = await response.text()
    assert "Hello from CI/CD pipeline!" in text

    await client.close()


def test_handle_returns_200():
    asyncio.run(_test_handle_returns_200())


if __name__ == "__main__":
    test_handle_returns_200()
    print("[OK] Wszystkie testy przeszly.")