"""
Ad_12. WebSockets i GraphQL
GraphQL z filtrowaniem.

Rozszerzenie API z Zadania 10 o:
- posts(authorId): zwraca posty przefiltrowane po autorze
  (jeśli authorId nie podano, zwraca wszystkie posty)
- searchUsers(name): wyszukuje użytkowników, których imię
  zawiera podany fragment tekstu (wyszukiwanie częściowe,
  bez rozróżniania wielkości liter)
"""

import strawberry
from typing import List, Optional
from aiohttp import web
from strawberry.aiohttp.views import GraphQLView


@strawberry.type
class Post:
    id: int
    title: str
    content: str
    author_id: strawberry.Private[int]

    @strawberry.field
    def author(self) -> Optional["User"]:
        for u in fake_users_db:
            if u.id == self.author_id:
                return u
        return None


@strawberry.type
class User:
    id: int
    name: str
    email: str

    @strawberry.field
    def posts(self) -> List[Post]:
        return [p for p in fake_posts_db if p.author_id == self.id]


fake_users_db: List[User] = [
    User(id=1, name="Jan Kowalski", email="jan@example.com"),
    User(id=2, name="Anna Nowak", email="anna@example.com"),
    User(id=3, name="Jan Wiśniewski", email="jan.w@example.com"),
]

fake_posts_db: List[Post] = [
    Post(id=1, title="Python jest super", content="...", author_id=1),
    Post(id=2, title="GraphQL tutorial", content="...", author_id=1),
    Post(id=3, title="Asynchroniczność", content="...", author_id=2),
]


@strawberry.type
class Query:
    """
    Główny typ zapytań GraphQL, rozszerzony o filtrowanie.
    """

    @strawberry.field
    def user(self, id: int) -> Optional[User]:
        for u in fake_users_db:
            if u.id == id:
                return u
        return None

    @strawberry.field
    def users(self) -> List[User]:
        return fake_users_db

    @strawberry.field
    def post(self, id: int) -> Optional[Post]:
        for p in fake_posts_db:
            if p.id == id:
                return p
        return None

    @strawberry.field
    def posts(self, author_id: Optional[int] = None) -> List[Post]:
        """
        Zwraca listę postów, opcjonalnie przefiltrowaną po ID autora.

        Jeśli author_id nie zostanie podane, zwraca WSZYSTKIE posty.
        Jeśli zostanie podane, zwraca tylko posty tego autora.
        """
        if author_id is None:
            return fake_posts_db
        return [p for p in fake_posts_db if p.author_id == author_id]

    @strawberry.field
    def search_users(self, name: str) -> List[User]:
        """
        Wyszukuje użytkowników, których imię zawiera podany
        fragment tekstu (wyszukiwanie częściowe, bez rozróżniania
        wielkości liter).
        """
        name_lower = name.lower()
        return [u for u in fake_users_db if name_lower in u.name.lower()]


schema = strawberry.Schema(query=Query)

app = web.Application()
app.router.add_route("*", "/graphql", GraphQLView(schema=schema))


if __name__ == '__main__':
    print("🚀 GraphQL API z filtrowaniem działa na http://localhost:8000/graphql")
    web.run_app(app, host='localhost', port=8000)