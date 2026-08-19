"""
Zadanie domowe 9 - Wprowadzenie do Django REST Framework
Relacje w API - Author, Book i StringRelatedField.

Kompletne rozwiązanie zadania obejmuje modele, serializatory
i ViewSety dla dwóch powiązanych modeli, gdzie BookSerializer
wyświetla nazwę autora zamiast samego ID.

============================================================
1. MODELE (library/models.py)
============================================================
"""

from django.db import models


class Author(models.Model):
    """
    Model reprezentujący autora książki.
    """

    name = models.CharField(
        max_length=200,
        verbose_name="Nazwa autora"
    )

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Model reprezentujący książkę, powiązany z autorem
    relacją ForeignKey.
    """

    title = models.CharField(
        max_length=200,
        verbose_name="Tytuł"
    )
    publication_year = models.IntegerField(
        verbose_name="Rok wydania"
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',
        verbose_name="Autor"
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year})"


"""
============================================================
2. SERIALIZATORY (library/serializers.py) - pełna zawartość:
============================================================

from rest_framework import serializers
from .models import Author, Book


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']


class BookSerializer(serializers.ModelSerializer):
    '''
    Pole 'author' służy do zapisu (przyjmuje ID autora).
    Pole 'author_name' jest tylko do odczytu i pokazuje nazwę
    autora zamiast ID, dzięki StringRelatedField.
    '''

    author_name = serializers.StringRelatedField(source='author', read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author', 'author_name']

============================================================
3. VIEWSETY (library/views.py) - pełna zawartość:
============================================================

from rest_framework import viewsets
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

============================================================
4. ROUTER (taskmanger/urls.py) - fragment do dodania:
============================================================

from library import views as library_views

router.register(r'authors', library_views.AuthorViewSet)
router.register(r'books', library_views.BookViewSet)

============================================================
5. WYNIKI TESTÓW W POSTMANIE
============================================================

Test 1: POST /api/authors/
Body: {"name": "Adam Mickiewicz"}
Response: 201 Created

Test 2: POST /api/books/
Body: {"title": "Pan Tadeusz", "publication_year": 1834, "author": 1}
Response: 201 Created

Test 3: GET /api/books/
Response: 200 OK
[
    {
        "id": 1,
        "title": "Pan Tadeusz",
        "publication_year": 1834,
        "author": 1,
        "author_name": "Adam Mickiewicz"
    }
]

Napotkany problem i rozwiązanie:
Pierwsza próba użycia samego StringRelatedField bezpośrednio jako
pola 'author' spowodowała błąd 500 (IntegrityError: NOT NULL
constraint failed: library_book.author_id), ponieważ
StringRelatedField jest domyślnie tylko do odczytu i nie
przyjmuje wartości przy zapisie (POST). Rozwiązaniem było
dodanie osobnego pola 'author_name' (read_only=True) obok
zwykłego, zapisywalnego pola 'author'.
"""