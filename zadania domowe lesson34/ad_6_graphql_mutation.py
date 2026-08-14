"""
Ad_6. WebSockets i GraphQL
GraphQL Mutation.

Rozszerzenie API z Zadania 5 o mutację "createUser", która dodaje
nowego użytkownika do fake bazy danych i zwraca go.
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
    Główny typ zapytań GraphQL (odczyt danych).
    """

    @strawberry.field
    def user(self, id: int) -> Optional[User]:
        """Zwraca użytkownika o podanym ID, albo None."""
        for u in fake_users_db:
            if u.id == id:
                return u
        return None

    @strawberry.field
    def users(self) -> List[User]:
        """Zwraca listę wszystkich użytkowników."""
        return fake_users_db


@strawberry.type
class Mutation:
    """
    Główny typ mutacji GraphQL (modyfikacje danych).
    """

    @strawberry.mutation
    def create_user(self, name: str, email: str) -> User:
        """
        Tworzy nowego użytkownika, dodaje go do fake bazy danych
        i zwraca utworzony obiekt.

        Nowe ID jest wyliczane jako maksymalne istniejące ID + 1,
        żeby zawsze było unikalne.
        """
        new_id = max(u.id for u in fake_users_db) + 1
        new_user = User(id=new_id, name=name, email=email)
        fake_users_db.append(new_user)
        return new_user


# Schemat zawiera teraz zarówno Query, jak i Mutation
schema = strawberry.Schema(query=Query, mutation=Mutation)

app = web.Application()
app.router.add_route("*", "/graphql", GraphQLView(schema=schema))


if __name__ == '__main__':
    print("🚀 GraphQL API działa na http://localhost:8000/graphql")
    web.run_app(app, host='localhost', port=8000)