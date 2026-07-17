"""
Zadanie domowe 8 - Cache w Django REST Framework
Różne czasy cache dla różnych metod ViewSetu.

============================================================
VIEWSET (products/views.py)
============================================================
"""

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint pozwalający na przeglądanie i edycję produktów.

    Różne metody mają różne czasy cachowania:
    - list (GET /products/) - 10 minut
    - retrieve (GET /products/{id}/) - 1 minuta
    - create, update, partial_update, destroy - brak cache
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @method_decorator(cache_page(60 * 10))  # 10 minut
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60))  # 1 minuta
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # create, update, partial_update, destroy pozostają
    # niezmienione - brak dekoratora oznacza brak cachowania.


"""
============================================================
WYNIKI TESTÓW W POSTMANIE
============================================================

Test 1: GET /api/products/ (list, cache 10 minut)
1. zapytanie: 472 ms (dane z bazy)
2. zapytanie: 32 ms (dane z cache) - znaczące przyspieszenie

Test 2: GET /api/products/1/ (retrieve, cache 1 minuta)
1. zapytanie: 66 ms (dane z bazy)
2. zapytanie: 29 ms (dane z cache) - przyspieszenie

Test 3: POST /api/products/ (create, bez cache)
Response: 201 Created (50 ms) - operacja zapisu działa normalnie,
bez ingerencji cache, co jest zgodne z oczekiwaniami - nowe dane
są od razu widoczne w bazie.

Wniosek

@method_decorator(cache_page(...)) pozwala zastosować różne
strategie cachowania dla różnych metod tego samego ViewSetu.
Krótszy czas cache dla retrieve (1 min) niż dla list (10 min)
ma sens - szczegóły pojedynczego obiektu mogą wymagać częstszej
aktualizacji, podczas gdy ogólna lista zmienia się rzadziej.
Operacje modyfikujące dane (create/update/destroy) pozostają
niecachowane, żeby zawsze poprawnie zapisywać zmiany.
"""