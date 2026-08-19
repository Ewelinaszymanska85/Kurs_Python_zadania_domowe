"""
Zadanie domowe 3 - Wprowadzenie do Django REST Framework
Pierwszy ViewSet i Router - Product.

Kompletne rozwiązanie zadania obejmuje dwa elementy:
1. ViewSet ProductViewSet (poniżej, aktywny kod)
2. Rejestracja w routerze w głównym urls.py (dołączona jako
   komentarz referencyjny)

============================================================
1. VIEWSET (products/views.py)
============================================================
"""

from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint pozwalający na przeglądanie i edycję produktów.

    ModelViewSet automatycznie udostępnia pełen zestaw operacji CRUD:
    - GET /products/ - lista wszystkich produktów
    - POST /products/ - stworzenie nowego produktu
    - GET /products/{id}/ - szczegóły jednego produktu
    - PUT/PATCH /products/{id}/ - aktualizacja produktu
    - DELETE /products/{id}/ - usunięcie produktu
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


"""
============================================================
2. ROUTER (taskmanger/urls.py) - fragment do dodania:
============================================================

from django.urls import path, include
from rest_framework import routers
from products import views as products_views

router = routers.DefaultRouter()
router.register(r'products', products_views.ProductViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]

============================================================
ODPOWIEDŹ NA PYTANIE Z TREŚCI ZADANIA:
"Uruchom serwer i wejdź na adres http://127.0.0.1:8000/api/products/
w przeglądarce. Co widzisz?"
============================================================

Po wejściu na ten adres widoczny jest przeglądarkowy interfejs API
Django REST Framework (tzw. "Browsable API"). Zawiera on:
- Nagłówek z nazwą endpointu ("Product List") i jego opisem
  (docstring z klasy ProductViewSet)
- Surową odpowiedź HTTP (status 200 OK, nagłówki, treść JSON - 
  w tym przypadku pusta lista [], bo baza nie ma jeszcze produktów)
- Interaktywny formularz HTML na dole strony, pozwalający wysłać
  zapytanie POST bezpośrednio z przeglądarki (pola: Nazwa, Cena)
  bez potrzeby używania Postmana czy innego narzędzia.

To ogromna zaleta DRF - to samo API obsługuje zarówno żądania
z przeglądarki (HTML), jak i z zewnętrznych programów (czysty JSON),
w zależności od nagłówka Accept w zapytaniu.
"""