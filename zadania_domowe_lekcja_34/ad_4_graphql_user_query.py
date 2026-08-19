"""
Ad_4. WebSockets i GraphQL
GraphQL - Query użytkownika.

Prosty serwer GraphQL z typem User (id, name, email) oraz
zapytaniem "user(id: ID!)" zwracającym użytkownika z fake listy
danych (symulacja bazy danych).
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


# Fake baza danych (lista przykładowych użytkowników)
fake_users_db: List[User] = [
    User(id=1, name="Jan Kowalski", email="jan@example.com"),
    User(id=2, name="Anna Nowak", email="anna@example.com"),
    User(id=3, name="Piotr Wiśniewski", email="piotr@example.com"),
]


@strawberry.type
class Query:
    """
    Główny typ zapytań GraphQL - punkt wejścia do odczytu danych.
    """

    @strawberry.field
    def user(self, id: int) -> Optional[User]:
        """
        Zwraca użytkownika o podanym ID, albo None jeśli nie
        znaleziono takiego użytkownika w fake bazie danych.
        """
        for u in fake_users_db:
            if u.id == id:
                return u
        return None


# Tworzenie schematu GraphQL (tylko Query, bez Mutation na razie)
schema = strawberry.Schema(query=Query)

app = web.Application()

# Endpoint GraphQL z włączonym interfejsem GraphiQL (do testowania
# zapytań bezpośrednio w przeglądarce)
app.router.add_route("*", "/graphql", GraphQLView(schema=schema))  


if __name__ == '__main__':
    print("🚀 GraphQL API działa na http://localhost:8000/graphql")
    print("📊 Otwórz w przeglądarce, aby użyć GraphiQL interface")
    web.run_app(app, host='localhost', port=8000)