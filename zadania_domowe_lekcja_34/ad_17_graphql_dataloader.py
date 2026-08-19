"""
Ad_17. WebSockets i GraphQL
GraphQL DataLoader.

Rozwiązanie problemu N+1 queries przy pobieraniu użytkowników
i ich postów. Bez DataLoadera, pobranie N użytkowników wraz
z ich postami wykonałoby 1 zapytanie o użytkowników + N osobnych
zapytań o posty każdego z nich (stąd nazwa "N+1"). DataLoader
grupuje (batchuje) te N zapytań w JEDNO, zbiorcze zapytanie.
"""

import strawberry
from typing import List, Optional
from aiohttp import web
from strawberry.aiohttp.views import GraphQLView
from strawberry.dataloader import DataLoader


@strawberry.type
class Post:
    id: int
    title: str
    author_id: strawberry.Private[int]


fake_users_db = [
    {"id": 1, "name": "Jan Kowalski", "email": "jan@example.com"},
    {"id": 2, "name": "Anna Nowak", "email": "anna@example.com"},
    {"id": 3, "name": "Piotr Wiśniewski", "email": "piotr@example.com"},
]

fake_posts_db = [
    Post(id=1, title="Post Jana 1", author_id=1),
    Post(id=2, title="Post Jana 2", author_id=1),
    Post(id=3, title="Post Anny 1", author_id=2),
    Post(id=4, title="Post Piotra 1", author_id=3),
]


async def batch_load_posts_by_author(author_ids: List[int]) -> List[List[Post]]:
    """
    Funkcja wsadowa (batch) wywoływana przez DataLoader.

    Zamiast wykonywać osobne zapytanie "SELECT * FROM posts WHERE
    author_id = X" dla KAŻDEGO użytkownika z osobna, DataLoader
    zbiera wszystkie potrzebne author_id w jednej turze i przekazuje
    je TUTAJ, jako listę - dzięki czemu możemy pobrać wszystkie
    potrzebne posty JEDNYM zapytaniem (tu: jedną pętlą po fake
    bazie, w prawdziwej aplikacji: jednym "WHERE author_id IN (...)").

    WAŻNE: kolejność zwracanej listy MUSI odpowiadać kolejności
    author_ids - DataLoader dopasowuje wyniki po indeksie.
    """
    print(f"🔄 DataLoader: pobieram posty dla autorów {author_ids} JEDNYM zapytaniem")

    result = []
    for author_id in author_ids:
        posts_for_author = [p for p in fake_posts_db if p.author_id == author_id]
        result.append(posts_for_author)

    return result


@strawberry.type
class User:
    id: int
    name: str
    email: str

    @strawberry.field
    async def posts(self, info: strawberry.Info) -> List[Post]:
        """
        Zwraca posty tego użytkownika, korzystając z DataLoadera
        przechowywanego w kontekście zapytania (info.context).

        Dzięki DataLoaderowi, jeśli GraphQL pyta o posty WIELU
        użytkowników w jednym zapytaniu, wszystkie te "żądania"
        zostaną zebrane i wykonane JEDNYM wywołaniem
        batch_load_posts_by_author, zamiast osobno dla każdego.
        """
        loader = info.context["posts_loader"]
        return await loader.load(self.id)


@strawberry.type
class Query:
    @strawberry.field
    def users(self) -> List[User]:
        return [User(**u) for u in fake_users_db]


schema = strawberry.Schema(query=Query)


class CustomGraphQLView(GraphQLView):
    """
    Rozszerzona wersja GraphQLView, która przy KAŻDYM zapytaniu
    tworzy NOWĄ instancję DataLoadera i umieszcza ją w kontekście.

    Nowa instancja dla każdego zapytania jest ważna - DataLoader
    "zbiera" żądania tylko w ramach jednego zapytania GraphQL,
    a potem powinien zostać odtworzony dla kolejnego.
    """
    async def get_context(self, request, response):
        return {
            "posts_loader": DataLoader(load_fn=batch_load_posts_by_author)
        }


app = web.Application()
app.router.add_route("*", "/graphql", CustomGraphQLView(schema=schema))


if __name__ == '__main__':
    print("🚀 GraphQL z DataLoader działa na http://localhost:8000/graphql")
    web.run_app(app, host='localhost', port=8000)