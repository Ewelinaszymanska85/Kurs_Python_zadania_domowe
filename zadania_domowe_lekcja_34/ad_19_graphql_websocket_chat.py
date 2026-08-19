"""
Ad_19. WebSockets i GraphQL
GraphQL + WebSocket chat.

Połączenie GraphQL i WebSocket w jednym systemie czatu:
- Query "messages": pobiera historię chatu (odpowiednik REST GET)
- Query "user": pobiera profil użytkownika
- Mutation "sendMessage": wysyła nową wiadomość (odpowiednik REST POST)
- Subscription "messageSent": nasłuchuje nowych wiadomości w czasie
  rzeczywistym (wykorzystuje WebSocket "pod spodem", tak jak
  w Zadaniu 15)
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


@strawberry.type
class Message:
    id: int
    content: str
    author_id: strawberry.Private[int]

    @strawberry.field
    def author(self) -> Optional[User]:
        for u in fake_users_db:
            if u.id == self.author_id:
                return u
        return None


fake_users_db: List[User] = [
    User(id=1, name="Ewelina"),
    User(id=2, name="Marek"),
]

# Historia wiadomości (przechowywana w pamięci)
messages_history: List[Message] = []

# Kolejki subskrybentów, nasłuchujących nowych wiadomości
message_queues: List[asyncio.Queue] = []


@strawberry.type
class Query:
    """
    Odczyt danych - historia chatu i profile użytkowników.
    """

    @strawberry.field
    def messages(self) -> List[Message]:
        """Zwraca całą historię wiadomości czatu."""
        return messages_history

    @strawberry.field
    def user(self, id: int) -> Optional[User]:
        """Zwraca profil użytkownika o podanym ID."""
        for u in fake_users_db:
            if u.id == id:
                return u
        return None


@strawberry.type
class Mutation:
    """
    Modyfikacja danych - wysyłanie nowych wiadomości.
    """

    @strawberry.mutation
    async def send_message(self, content: str, author_id: int) -> Message:
        """
        Tworzy nową wiadomość, dodaje ją do historii i natychmiast
        powiadamia wszystkich subskrybentów (przez kolejki).
        """
        new_id = len(messages_history) + 1
        new_message = Message(id=new_id, content=content, author_id=author_id)
        messages_history.append(new_message)

        # Powiadamiamy wszystkich aktywnych subskrybentów
        for queue in message_queues:
            await queue.put(new_message)

        return new_message


@strawberry.type
class Subscription:
    """
    Nasłuchiwanie nowych wiadomości w czasie rzeczywistym
    (wykorzystuje WebSocket "pod spodem").
    """

    @strawberry.subscription
    async def message_sent(self) -> AsyncGenerator[Message, None]:
        """
        Emituje każdą nową wiadomość natychmiast po jej wysłaniu
        przez mutację sendMessage.
        """
        queue: asyncio.Queue = asyncio.Queue()
        message_queues.append(queue)

        try:
            while True:
                new_message = await queue.get()
                yield new_message
        finally:
            message_queues.remove(queue)


schema = strawberry.Schema(query=Query, mutation=Mutation, subscription=Subscription)

app = web.Application()
app.router.add_route("*", "/graphql", GraphQLView(schema=schema))


if __name__ == '__main__':
    print("🚀 GraphQL + WebSocket chat działa na http://localhost:8000/graphql")
    web.run_app(app, host='localhost', port=8000)