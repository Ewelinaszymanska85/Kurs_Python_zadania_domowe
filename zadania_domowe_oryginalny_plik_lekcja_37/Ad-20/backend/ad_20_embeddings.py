import hashlib

import numpy as np


EMBEDDING_DIMENSIONS = 128


def generate_embedding(text: str) -> list[float]:
    """
    Generuje deterministyczny pseudo-embedding na podstawie tekstu.

    UWAGA: To symulacja zastępująca OpenAI Embeddings API (brak klucza API).
    Żeby użyć prawdziwego OpenAI, podmień tę funkcję na:

        from openai import OpenAI
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        response = client.embeddings.create(model="text-embedding-3-small", input=text)
        return response.data[0].embedding

    Reszta systemu (cache, podobieństwo kosinusowe, Celery) zadziała bez zmian.
    """
    words = text.lower().split()
    vector = np.zeros(EMBEDDING_DIMENSIONS)

    for word in words:
        word_hash = int(hashlib.md5(word.encode()).hexdigest(), 16)
        rng = np.random.default_rng(word_hash % (2**32))
        vector += rng.normal(size=EMBEDDING_DIMENSIONS)

    norm = np.linalg.norm(vector)

    if norm > 0:
        vector = vector / norm

    return vector.tolist()


def cosine_similarity(vector_a: list[float], vector_b: list[float]) -> float:
    """Oblicza podobieństwo kosinusowe między dwoma wektorami embeddingów."""
    a = np.array(vector_a)
    b = np.array(vector_b)

    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))