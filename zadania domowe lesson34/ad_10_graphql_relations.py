"""
Ad_10. WebSockets i GraphQL
GraphQL z relacjami.

API z typami User i Post, gdzie:
- User ma pole "posts" zwracające listę jego postów
- Post ma pole "author" zwracające autora tego posta

To pokazuje kluczową zaletę GraphQL - możliwość pobrania
powiązanych danych (relacji) w jednym zapytaniu.
"""

import strawberry
from typing import List, Optional
from aiohttp import web
from strawberry.aiohttp.views import GraphQLView


@strawberry.type
class Post:
    """
    Typ GraphQL reprezentujący post.

    Pole 'author' jest polem obliczanym (resolver) - zamiast
    przechowywać cały obiekt User bezpośrednio, przechowujemy
    tylko author_id, a pełny obiekt User wyszukujemy dynamicznie.
    """
    id: int
    title: str
    content: str
    author_id: strawberry.Private[int]  # ukryte przed schematem GraphQL

    @strawberry.field
    def author(self) -> Optional["User"]:
        """
        Zwraca autora tego posta, wyszukując go w fake bazie
        użytkowników po author_id.
        """
        for u in fake_users_db:
            if u.id == self.author_id:
                return u
        return None


@strawberry.type
class User:
    """
    Typ GraphQL reprezentujący użytkownika.
    """
    id: int
    name: str
    email: str

    @strawberry.field
    def posts(self) -> List[Post]:
        """
        Zwraca listę wszystkich postów napisanych przez tego
        użytkownika, filtrując fake bazę postów po author_id.
        """
        return [p for p in fake_posts_db if p.author_id == self.id]


# Fake bazy danych
fake_users_db: List[User] = [
    User(id=1, name="Jan Kowalski", email="jan@example.com"),
    User(id=2, name="Anna Nowak", email="anna@example.com"),
]

fake_posts_db: List[Post] = [
    Post(id=1, title="Python jest super", content="...", author_id=1),
    Post(id=2, title="GraphQL tutorial", content="...", author_id=1),
    Post(id=3, title="Asynchroniczność", content="...", author_id=2),
]


@strawberry.type
class Query:
    """
    Główny typ zapytań GraphQL.
    """

    @strawberry.field
    def user(self, id: int) -> Optional[User]:
        """Zwraca użytkownika o podanym ID."""
        for u in fake_users_db:
            if u.id == id:
                return u
        return None

    @strawberry.field
    def users(self) -> List[User]:
        """Zwraca listę wszystkich użytkowników."""
        return fake_users_db

    @strawberry.field
    def post(self, id: int) -> Optional[Post]:
        """Zwraca post o podanym ID."""
        for p in fake_posts_db:
            if p.id == id:
                return p
        return None


schema = strawberry.Schema(query=Query)

app = web.Application()
app.router.add_route("*", "/graphql", GraphQLView(schema=schema))


if __name__ == '__main__':
    print("🚀 GraphQL API z relacjami działa na http://localhost:8000/graphql")
    web.run_app(app, host='localhost', port=8000)