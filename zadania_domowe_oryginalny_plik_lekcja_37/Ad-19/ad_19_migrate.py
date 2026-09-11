import asyncio
import os

import asyncpg


async def run_migrations() -> None:
    """Tworzy wymagane tabele w bazie danych (symulacja migracji)."""
    connection = await asyncpg.connect(
        host=os.environ["DB_HOST"],
        port=os.environ.get("DB_PORT", "5432"),
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )

    print("[MIGRATE] Uruchamiam migracje...")

    await connection.execute(
        "CREATE TABLE IF NOT EXISTS items (id SERIAL PRIMARY KEY, name TEXT NOT NULL)"
    )
    await connection.execute(
        "CREATE TABLE IF NOT EXISTS admins (id SERIAL PRIMARY KEY, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL)"
    )

    count = await connection.fetchval("SELECT COUNT(*) FROM items")
    if count == 0:
        await connection.execute(
            "INSERT INTO items (name) VALUES ('Pierwszy element'), ('Drugi element')"
        )

    await connection.close()

    print("[MIGRATE] Migracje zakonczone pomyslnie.")


if __name__ == "__main__":
    asyncio.run(run_migrations())