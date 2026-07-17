"""
Zadanie domowe 1 - Lekcja 28
Dokumentacja API z drf-spectacular (OpenAPI / Swagger UI).

Zadanie zrealizowane na bazie istniejącego projektu "cacheproject"
z Lekcji 27 (ProductViewSet + product_summary_view), rozbudowanego
teraz o automatyczną i ręcznie dostosowaną dokumentację API.

============================================================
1. INSTALACJA
============================================================

pip install drf-spectacular

============================================================
2. KONFIGURACJA (cacheproject/settings.py)
============================================================
"""

INSTALLED_APPS_fragment = [
    # ... pozostałe aplikacje bez zmian
    'rest_framework',
    'drf_spectacular',   # nowa aplikacja - generator schematu OpenAPI
    'products',
    'debug_toolbar',
]

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Cache Project API',
    'DESCRIPTION': 'Dokumentacja API dla projektu cacheproject (produkty, cache).',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

"""
============================================================
3. ŚCIEŻKI URL (cacheproject/urls.py) - fragment dodany
============================================================

from drf_spectacular.views import (
    SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
)

urlpatterns += [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

============================================================
4. DOSTOSOWANIE DOKUMENTACJI - @extend_schema (products/views.py)
============================================================

Do ProductViewSet i product_summary_view dodano dekoratory
@extend_schema z trzech różnych przykładów pokazanych na lekcji:

a) summary + description + tags
   - zastosowane m.in. na product_summary_view i retrieve

b) parametry zapytania (OpenApiParameter)
   - zastosowane na metodzie list (parametr 'name' - dokumentuje
     planowaną możliwość filtrowania produktów po nazwie)

c) różne kody odpowiedzi (OpenApiResponse)
   - zastosowane na retrieve (200 i 404) oraz product_summary_view (200)

Przykładowy fragment (metoda retrieve):

    @extend_schema(
        summary="Pobierz szczegóły jednego produktu",
        description=(
            "Zwraca szczegóły pojedynczego produktu. Wynik jest buforowany "
            "na 1 minutę przy pomocy niskopoziomowego API cache z własnym "
            "kluczem (product_detail_<id>), co pozwala na precyzyjne "
            "unieważnianie cache po aktualizacji obiektu."
        ),
        tags=['Produkty'],
        responses={
            200: OpenApiResponse(description="Szczegóły produktu (z cache lub bazy danych)"),
            404: OpenApiResponse(description="Nie znaleziono produktu o podanym ID"),
        }
    )
    def retrieve(self, request, *args, **kwargs):
        ...

Dodatkowo, dla spójności dokumentacji, do pozostałych metod
ViewSetu (create, update, partial_update, destroy) dodano
@extend_schema(tags=['Produkty']) - samą etykietę bez dodatkowego
opisu, żeby wszystkie operacje CRUD trafiły do jednej, wspólnej
grupy "Produkty" w Swagger UI, zamiast być rozbite na dwie
oddzielne grupy ("Produkty" i domyślnie wygenerowane "products").

============================================================
WERYFIKACJA
============================================================

Po uruchomieniu serwera (python manage.py runserver) i wejściu
na http://127.0.0.1:8000/api/schema/swagger-ui/ wyświetliła się
interaktywna dokumentacja API z tytułem "Cache Project API"
i wersją 1.0.0.

Wszystkie endpointy zostały poprawnie pogrupowane pod wspólnym
tagiem "Produkty":

GET    /api/product-summary/     - "Podsumowanie produktów z cache"
GET    /api/products/            - "Lista produktów (cache 10 minut)"
POST   /api/products/
GET    /api/products/{id}/       - "Pobierz szczegóły jednego produktu"
PUT    /api/products/{id}/
PATCH  /api/products/{id}/
DELETE /api/products/{id}/

Napotkana obserwacja

Przy pierwszej próbie, metody create/update/partial_update/destroy
nie miały żadnego dekoratora @extend_schema, przez co
drf-spectacular umieścił je w OSOBNEJ, automatycznie wygenerowanej
grupie "products" (mała litera, nazwa na podstawie ViewSetu),
podczas gdy list/retrieve trafiły do ręcznie nazwanej grupy
"Produkty". Dopiero dodanie @extend_schema(tags=['Produkty']) do
pozostałych metod scaliło wszystko w jedną, spójną grupę. Pokazuje
to, że tagowanie w drf-spectacular trzeba stosować konsekwentnie
do WSZYSTKICH metod danego widoku, a nie tylko wybranych - inaczej
dokumentacja robi się niespójna.

Wniosek

drf-spectacular pozwala w prosty sposób (kilka linii konfiguracji
w settings.py i urls.py) wygenerować w pełni interaktywną
dokumentację API zgodną ze standardem OpenAPI. Automatyczna
analiza kodu (docstringi, serializery, routing) daje solidny
punkt wyjścia, a dekorator @extend_schema pozwala doprecyzować
opisy, parametry zapytania i możliwe kody odpowiedzi - co czyni
dokumentację czytelną i użyteczną zarówno dla innych programistów,
jak i dla samej autorki, wracającej do projektu po czasie.
""" 