"""
Ad_5. WebSockets i GraphQL
GraphQL - Lista użytkowników.

Rozszerzenie API z Zadania 4 o zapytanie "users" zwracające
listę WSZYSTKICH użytkowników z fake bazy danych.
"""

import strawberry
from typing import Optional, List
from aiohttp import web
from strawberry.aiohttp.views import GraphQLView


@strawberry.type
class User:
    """
    Typ GraphQL reprezentujący użytkownika.
    """
    id: int
    name: str
    email: str


fake_users_db: List[User] = [
    User(id=1, name="Jan Kowalski", email="jan@example.com"),
    User(id=2, name="Anna Nowak", email="anna@example.com"),
    User(id=3, name="Piotr Wiśniewski", email="piotr@example.com"),
]


@strawberry.type
class Query:
    """
    Główny typ zapytań GraphQL.
    """

    @strawberry.field
    def user(self, id: int) -> Optional[User]:
        """
        Zwraca użytkownika o podanym ID, albo None jeśli nie
        znaleziono.
        """
        for u in fake_users_db:
            if u.id == id:
                return u
        return None

    @strawberry.field
    def users(self) -> List[User]:
        """
        Zwraca listę WSZYSTKICH użytkowników z fake bazy danych.
        """
        return fake_users_db


schema = strawberry.Schema(query=Query)

app = web.Application()
app.router.add_route("*", "/graphql", GraphQLView(schema=schema))


if __name__ == '__main__':
    print("🚀 GraphQL API działa na http://localhost:8000/graphql")
    web.run_app(app, host='localhost', port=8000)