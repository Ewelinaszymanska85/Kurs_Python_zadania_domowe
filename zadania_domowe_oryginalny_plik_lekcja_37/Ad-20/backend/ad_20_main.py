import os
from contextlib import asynccontextmanager

import asyncpg
import numpy as np
import redis.asyncio as redis
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ad_20_embeddings import generate_embedding, cosine_similarity
from ad_20_tasks import celery_app, generate_recommendations_task


class BookCreate(BaseModel):
    title: str
    description: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db_pool = await asyncpg.create_pool(
        host=os.environ["DB_HOST"],
        port=os.environ.get("DB_PORT", "5432"),
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )
    app.state.redis = redis.Redis(host="redis", port=6379, decode_responses=True)

    async with app.state.db_pool.acquire() as connection:
        await connection.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                embedding FLOAT8[] NOT NULL
            )
            """
        )

        count = await connection.fetchval("SELECT COUNT(*) FROM books")

        if count == 0:
            sample_books = [
                ("Wiedzmin", "Fantasy o wiedzminie walczacym z potworami w mrocznym swiecie"),
                ("Diuna", "Science fiction o pustynnej planecie i przyprawie zmieniajacej losy galaktyki"),
                ("Zbrodnia i kara", "Psychologiczny dramat o zbrodni, winie i odkupieniu w carskiej Rosji"),
                ("Fundacja", "Science fiction o upadku galaktycznego imperium i psychohistorii"),
                ("Hobbit", "Fantasy o wyprawie hobbita po skarb strzezony przez smoka"),
            ]

            for title, description in sample_books:
                embedding = generate_embedding(description)
                await connection.execute(
                    "INSERT INTO books (title, description, embedding) VALUES ($1, $2, $3)",
                    title, description, embedding,
                )

    yield

    await app.state.db_pool.close()
    await app.state.redis.close()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8082"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/books")
async def list_books():
    async with app.state.db_pool.acquire() as connection:
        rows = await connection.fetch("SELECT id, title, description FROM books ORDER BY id")

    return [dict(row) for row in rows]


@app.post("/books", status_code=201)
async def create_book(book: BookCreate):
    embedding = generate_embedding(book.description)

    async with app.state.db_pool.acquire() as connection:
        row = await connection.fetchrow(
            "INSERT INTO books (title, description, embedding) VALUES ($1, $2, $3) RETURNING id, title, description",
            book.title, book.description, embedding,
        )

    return dict(row)


@app.get("/recommendations/{book_id}")
async def get_recommendations(book_id: int):
    """Zwraca rekomendacje z cache, lub zleca ich wygenerowanie w tle przez Celery."""
    cache_key = f"recommendations:{book_id}"
    cached = await app.state.redis.get(cache_key)

    if cached is not None:
        import json
        return {"source": "cache", "recommendations": json.loads(cached)}

    task = generate_recommendations_task.delay(book_id)

    return {"source": "queued", "task_id": task.id}


@app.get("/recommendations/status/{task_id}")
async def get_recommendation_status(task_id: str):
    task_result = celery_app.AsyncResult(task_id)

    response = {"task_id": task_id, "status": task_result.status}

    if task_result.ready():
        response["result"] = task_result.result

    return response