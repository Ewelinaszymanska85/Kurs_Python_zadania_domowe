"""
Zadanie domowe 3 - Cache w Django REST Framework
Cachowanie widoku API - @cache_page na 60 sekund.

Kompletne rozwiązanie zadania obejmuje ProductViewSet z cachowaną
metodą list(), oraz wyniki weryfikacji w Django Debug Toolbar.

============================================================
WIDOK (products/views.py)
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

    Metoda 'list' (GET /api/products/) jest cachowana na 60 sekund.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @method_decorator(cache_page(60))
    def list(self, request, *args, **kwargs):
        """
        Zwraca listę wszystkich produktów, buforowaną na 60 sekund.
        """
        return super().list(request, *args, **kwargs)


"""
============================================================
WYNIKI WERYFIKACJI W DJANGO DEBUG TOOLBAR
============================================================

Pierwsze żądanie (po restarcie serwera / wyczyszczeniu cache):
Total calls: 3 | Cache hits: 0 | Cache misses: 1
Operacje: 1x get (miss), 2x set (zapis odpowiedzi do cache na 60s)

Kolejne żądanie z tego samego źródła (w ciągu 60 sekund):
Total calls: 2 | Cache hits: 2 | Cache misses: 0
Operacje: 2x get (oba trafienia - dane pobrane z cache)

Napotkana trudność

Django Debug Toolbar tworzy OSOBNE klucze cache w zależności od
nagłówka Accept żądania - żądanie z przeglądarki (oczekującej HTML
w ramach DRF Browsable API) i żądanie z Postmana (oczekującego
czystego application/json) trafiają w RÓŻNE wpisy cache, mimo
tego samego adresu URL. Dopiero porównanie dwóch kolejnych żądań
z tego samego źródła (oba z przeglądarki, albo oba z Postmana)
pozwoliło poprawnie zaobserwować przejście miss -> hit.

Wniosek

@cache_page skutecznie buforuje całą odpowiedź HTTP na czas
określony w parametrze (tutaj: 60 sekund), znacząco redukując
czas obsługi kolejnych, identycznych żądań - drugie i kolejne
zapytania nie odpytują już bazy danych.
"""