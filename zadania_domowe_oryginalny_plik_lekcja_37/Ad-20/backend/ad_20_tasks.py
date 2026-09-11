import json
import os

import asyncpg
from celery import Celery

from ad_20_embeddings import cosine_similarity

celery_app = Celery(
    "ad_20_tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/1",
)


@celery_app.task(name="generate_recommendations")
def generate_recommendations_task(book_id: int) -> dict:
    """Znajduje najbardziej podobne książki na podstawie embeddingów (długie zadanie w tle)."""
    import asyncio
    import redis as redis_sync

    async def _run() -> dict:
        connection = await asyncpg.connect(
            host=os.environ["DB_HOST"],
            port=os.environ.get("DB_PORT", "5432"),
            database=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
        )

        target_book = await connection.fetchrow(
            "SELECT id, title, embedding FROM books WHERE id = $1", book_id,
        )

        if target_book is None:
            await connection.close()
            return {"error": "Ksiazka nie znaleziona"}

        all_books = await connection.fetch(
            "SELECT id, title, embedding FROM books WHERE id != $1", book_id,
        )

        await connection.close()

        scored_books = [
            {
                "id": book["id"],
                "title": book["title"],
                "similarity": cosine_similarity(target_book["embedding"], book["embedding"]),
            }
            for book in all_books
        ]

        scored_books.sort(key=lambda item: item["similarity"], reverse=True)
        top_recommendations = scored_books[:3]

        redis_client = redis_sync.Redis(host="redis", port=6379, decode_responses=True)
        redis_client.set(
            f"recommendations:{book_id}",
            json.dumps(top_recommendations),
            ex=300,
        )
        redis_client.close()

        return {"book_id": book_id, "recommendations": top_recommendations}

    return asyncio.run(_run())