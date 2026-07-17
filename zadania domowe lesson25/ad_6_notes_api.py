"""
Zadanie domowe 6 - Wprowadzenie do Django REST Framework
API do notatek - pełne CRUD dla modelu Note.

Kompletne rozwiązanie zadania obejmuje model, serializator, ViewSet
oraz wyniki testów wszystkich 5 operacji CRUD przeprowadzonych
w Postmanie.

============================================================
1. MODEL (notes/models.py)
============================================================
"""

from django.db import models


class Note(models.Model):
    """
    Model reprezentujący pojedynczą notatkę.

    Pola:
        title (str): Tytuł notatki.
        content (str): Treść notatki.
        created_at (datetime): Data i czas utworzenia notatki.
    """

    title = models.CharField(
        max_length=200,
        verbose_name="Tytuł"
    )
    content = models.TextField(
        verbose_name="Treść"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data utworzenia"
    )

    def __str__(self):
        return self.title


"""
============================================================
2. SERIALIZATOR (notes/serializers.py) - pełna zawartość:
============================================================

from rest_framework import serializers
from .models import Note


class NoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'created_at']

============================================================
3. VIEWSET (notes/views.py) - pełna zawartość:
============================================================

from rest_framework import viewsets
from .models import Note
from .serializers import NoteSerializer


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all().order_by('-created_at')
    serializer_class = NoteSerializer

============================================================
4. ROUTER (taskmanger/urls.py) - fragment do dodania:
============================================================

from notes import views as notes_views

router.register(r'notes', notes_views.NoteViewSet)

============================================================
5. WYNIKI TESTÓW W POSTMANIE (5 operacji CRUD)
============================================================

1. CREATE (POST) /api/notes/
   Request body:
   {"title": "Notatka testowa", "content": "To jest treść mojej pierwszej notatki."}
   Response: 201 Created
   {"id": 1, "title": "Notatka testowa", "content": "...", "created_at": "2026-07-08T07:30:30.423029Z"}

2. READ - lista (GET) /api/notes/
   Response: 200 OK - lista wszystkich notatek w formacie JSON

3. READ - szczegóły (GET) /api/notes/1/
   Response: 200 OK
   {"id": 1, "title": "Notatka testowa", "content": "...", "created_at": "..."}

4. UPDATE (PUT) /api/notes/1/
   Request body:
   {"title": "Notatka zaktualizowana", "content": "Zmieniona treść notatki."}
   Response: 200 OK - zaktualizowany obiekt notatki

5. DELETE /api/notes/1/
   Response: 204 No Content - notatka usunięta pomyślnie z bazy danych
"""