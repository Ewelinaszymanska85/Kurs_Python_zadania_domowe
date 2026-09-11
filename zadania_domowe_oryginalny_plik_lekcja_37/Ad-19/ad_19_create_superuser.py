import asyncio
import os

import asyncpg


async def create_superuser_if_not_exists() -> None:
    """Tworzy konto superusera, jeśli jeszcze nie istnieje."""
    connection = await asyncpg.connect(
        host=os.environ["DB_HOST"],
        port=os.environ.get("DB_PORT", "5432"),
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )

    admin_username = os.environ.get("SUPERUSER_USERNAME", "admin")
    admin_password = os.environ.get("SUPERUSER_PASSWORD", "admin123")

    existing = await connection.fetchval(
        "SELECT id FROM admins WHERE username = $1", admin_username,
    )

    if existing is None:
        await connection.execute(
            "INSERT INTO admins (username, password) VALUES ($1, $2)",
            admin_username, admin_password,
        )
        print(f"[SUPERUSER] Utworzono superusera: {admin_username}")
    else:
        print(f"[SUPERUSER] Superuser '{admin_username}' juz istnieje, pomijam.")

    await connection.close()


if __name__ == "__main__":
    asyncio.run(create_superuser_if_not_exists())