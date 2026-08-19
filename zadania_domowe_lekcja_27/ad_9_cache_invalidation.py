"""
Zadanie domowe 9 - Cache w Django REST Framework
Unieważnianie cache po aktualizacji obiektu.

============================================================
VIEWSET (products/views.py)
============================================================
"""

from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    - retrieve używa niskopoziomowego API cache z własnym kluczem
      (product_detail_<id>), zamiast @cache_page, ponieważ własny
      klucz można precyzyjnie usunąć po aktualizacji obiektu.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @method_decorator(cache_page(60 * 10))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        cache_key = f'product_detail_{pk}'
        cached_data = cache.get(cache_key)

        if cached_data is not None:
            return Response(cached_data)

        response = super().retrieve(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60)
        return response

    def perform_update(self, serializer):
        """
        Po zapisaniu aktualizacji, usuwa klucz cache dla widoku
        szczegółów tego konkretnego produktu - unieważnienie cache.
        """
        instance = serializer.save()
        cache_key = f'product_detail_{instance.pk}'
        cache.delete(cache_key)

    def perform_destroy(self, instance):
        pk = instance.pk
        instance.delete()
        cache.delete(f'product_detail_{pk}')


"""
============================================================
WYNIKI TESTÓW W POSTMANIE
============================================================

Test 1: GET /api/products/1/ (pierwsze zapytanie)
405 ms - cache miss, dane pobrane z bazy

Test 2: GET /api/products/1/ (drugie zapytanie)
33 ms - cache hit, dane z cache

Test 3: PATCH /api/products/1/ {"name": "Laptop Dell - zaktualizowany"}
136 ms - aktualizacja zapisana, cache klucza product_detail_1 usunięty

Test 4: GET /api/products/1/ (zaraz po PATCH)
37 ms
{"id": 1, "name": "Laptop Dell - zaktualizowany", "price": "3500.00"}

KLUCZOWY WYNIK: Test 4 zwraca NOWĄ nazwę produktu, mimo szybkiego
czasu odpowiedzi (37 ms, świeżo zapisany cache) - potwierdza to,
że stary wpis cache został poprawnie unieważniony po aktualizacji,
zamiast zwracać przestarzałe dane z Testu 1/2.

Napotkana trudność i decyzja projektowa

@cache_page generuje automatyczne, złożone klucze cache (zależne
od pełnego URL i nagłówków żądania), które są trudne do
przewidzenia i ręcznego usunięcia. Dlatego dla metody retrieve
zrezygnowano z @cache_page na rzecz niskopoziomowego API cache
z WŁASNYM, czytelnym kluczem (product_detail_<id>) - to podejście
daje pełną kontrolę nad unieważnianiem cache dla konkretnego obiektu.

Wniosek

Nadpisanie perform_update() w ViewSetcie to wygodne miejsce do
unieważniania cache po aktualizacji - DRF wywołuje tę metodę
automatycznie po pomyślnej walidacji danych, zarówno dla PUT,
jak i PATCH (partial_update).
"""