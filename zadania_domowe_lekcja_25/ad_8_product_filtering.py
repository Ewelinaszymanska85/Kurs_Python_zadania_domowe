"""
Zadanie domowe 8 - Wprowadzenie do Django REST Framework
Filtrowanie i wyszukiwanie - filtrowanie produktów po cenie.

Kompletne rozwiązanie zadania obejmuje nadpisanie metody
get_queryset() w ProductViewSet, aby obsługiwała opcjonalne
parametry zapytania min_price i max_price.

============================================================
VIEWSET (products/views.py)
============================================================
"""

from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint pozwalający na przeglądanie i edycję produktów.

    Obsługuje filtrowanie po cenie za pomocą parametrów zapytania
    min_price i max_price, np.:
    /api/products/?min_price=100&max_price=200
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        """
        Nadpisuje domyślny queryset, dodając opcjonalne filtrowanie
        po cenie na podstawie parametrów zapytania min_price
        i max_price.

        Jeśli oba parametry są podane, zwraca produkty w podanym
        przedziale cenowym (włącznie z granicami). Jeśli podany
        jest tylko jeden z nich, filtruje tylko w tym kierunku.
        Jeśli żaden nie jest podany, zwraca wszystkie produkty.
        """
        queryset = Product.objects.all()

        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        if min_price is not None:
            queryset = queryset.filter(price__gte=min_price)

        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)

        return queryset


"""
============================================================
WYNIKI TESTÓW
============================================================

Test: /api/products/?min_price=100&max_price=300

Baza produktów przed filtrowaniem:
- Laptop Dell - 3500.00
- Mysz bezprzewodowa - 89.99
- Klawiatura mechaniczna - 249.50

Wynik zapytania (HTTP 200 OK):
[
    {
        "id": 2,
        "name": "Klawiatura mechaniczna",
        "price": "249.50"
    }
]

Tylko "Klawiatura mechaniczna" mieści się w przedziale 100-300,
co potwierdza poprawne działanie filtrowania po cenie.
"""