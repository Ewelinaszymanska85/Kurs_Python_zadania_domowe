"""
Zadanie domowe 10 - Wprowadzenie do Django REST Framework
Własna walidacja w serializatorze - validate_title dla notatek.

Kompletne rozwiązanie zadania obejmuje własną metodę walidacji
pola title w NoteSerializer, sprawdzającą minimalną długość tytułu.

============================================================
SERIALIZATOR (notes/serializers.py)
============================================================
"""

from rest_framework import serializers
from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    """
    Serializator modelu Note.

    Zawiera własną walidację pola title.
    """

    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'created_at']

    def validate_title(self, value):
        """
        Sprawdza, czy tytuł notatki ma co najmniej 5 znaków.

        DRF automatycznie wywołuje metody o nazwie
        'validate_<nazwa_pola>' podczas walidacji danych
        wejściowych, jeszcze przed zapisem obiektu do bazy.

        Args:
            value (str): Wartość pola title przesłana przez klienta.

        Returns:
            str: Ta sama wartość, jeśli walidacja przejdzie pomyślnie.

        Raises:
            serializers.ValidationError: Jeśli tytuł jest krótszy
                niż 5 znaków.
        """
        if len(value) < 5:
            raise serializers.ValidationError(
                "Tytuł notatki musi mieć co najmniej 5 znaków."
            )
        return value


"""
============================================================
WYNIKI TESTÓW W POSTMANIE
============================================================

Test 1: POST /api/notes/ - za krótki tytuł
Body: {"title": "Ab", "content": "Treść notatki z za krótkim tytułem."}
Response: 400 Bad Request
{
    "title": [
        "Tytuł notatki musi mieć co najmniej 5 znaków."
    ]
}

Test 2: POST /api/notes/ - poprawny tytuł
Body: {"title": "Zakupy", "content": "Kupić mleko i chleb."}
Response: 201 Created
{
    "id": 2,
    "title": "Zakupy",
    "content": "Kupić mleko i chleb.",
    "created_at": "2026-07-08T08:20:47.264192Z"
}

Wniosek: Metoda validate_title poprawnie odrzuca zbyt krótkie
tytuły (błąd 400 z czytelnym komunikatem), jednocześnie
przepuszczając prawidłowe dane bez zakłóceń.
"""