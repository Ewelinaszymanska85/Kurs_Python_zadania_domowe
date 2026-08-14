"""
Ad_15. WebSockets i GraphQL
GraphQL Subscription.

Subskrypcja GraphQL emitująca event za każdym razem, gdy nowy
użytkownik zostanie zarejestrowany przez mutację createUser.
Subskrypcje w Strawberry wykorzystują WebSocket "pod spodem",
mimo że korzystamy z tego samego, znanego już schematu GraphQL.
"""

import asyncio
import strawberry
from typing import List, Optional, AsyncGenerator
from aiohttp import web
from strawberry.aiohttp.views import GraphQLView


@strawberry.type
class User:
    id: int
    name: str
    email: str


fake_users_db: List[User] = [
    User(id=1, name="Jan Kowalski", email="jan@example.com"),
]

# Kolejka używana do przekazywania eventów "nowy użytkownik"
# do wszystkich aktywnych subskrypcji
new_user_queues: List[asyncio.Queue] = []


@strawberry.type
class Query:
    @strawberry.field
    def users(self) -> List[User]:
        return fake_users_db


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user(self, name: str, email: str) -> User:
        """
        Tworzy nowego użytkownika i powiadamia WSZYSTKIE aktywne
        subskrypcje o tym zdarzeniu, wkładając nowego użytkownika
        do każdej kolejki nasłuchujących klientów.
        """
        new_id = max(u.id for u in fake_users_db) + 1
        new_user = User(id=new_id, name=name, email=email)
        fake_users_db.append(new_user)

        # Powiadamiamy wszystkich subskrybentów o nowym użytkowniku
        for queue in new_user_queues:
            await queue.put(new_user)

        return new_user


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def user_registered(self) -> AsyncGenerator[User, None]:
        """
        Subskrypcja emitująca nowego użytkownika za każdym razem,
        gdy zostanie on utworzony przez mutację createUser.

        Działa poprzez własną kolejkę (Queue) - gdy mutacja doda
        coś do tej kolejki, generator natychmiast to "yielduje"
        do klienta nasłuchującego subskrypcji.
        """
        queue: asyncio.Queue = asyncio.Queue()
        new_user_queues.append(queue)

        try:
            while True:
                # Czekamy na nowego użytkownika w kolejce
                new_user = await queue.get()
                yield new_user
        finally:
            # Sprzątamy po sobie, gdy klient przestanie nasłuchiwać
            new_user_queues.remove(queue)


schema = strawberry.Schema(query=Query, mutation=Mutation, subscription=Subscription)

app = web.Application()
app.router.add_route("*", "/graphql", GraphQLView(schema=schema))


if __name__ == '__main__':
    print("🚀 GraphQL z subskrypcjami działa na http://localhost:8000/graphql")
    web.run_app(app, host='localhost', port=8000)