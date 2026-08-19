"""
Zadanie domowe 6 - Cache w Django REST Framework
Implementacja cache plikowego - FileBasedCache.

============================================================
KONFIGURACJA (cacheproject/settings.py)
============================================================
"""

import os

# Konfiguracja cache - pamięć podręczna zapisywana w plikach na dysku (FileBasedCache)
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": str(BASE_DIR / "django_cache"),
    }
} 
"""
============================================================
WYNIKI TESTU
============================================================

Po zmianie backendu na FileBasedCache i wejściu na widok
z Zadania 3 (GET /api/products/, cachowany przez @cache_page),
w katalogu projektu automatycznie pojawił się nowy folder
"django_cache" (Django tworzy go samo, przy pierwszym zapisie -
nie trzeba go tworzyć ręcznie), zawierający pliki:

62df46e8622f92af4adbcf60dfdacaf0.djcache - 2812 bytes
8705d8718a2fa0b764da175b5e517d23.djcache - 54 bytes

Co zawierają te pliki?

Pliki .djcache przechowują zserializowane (w formacie pickle)
dane Pythona - w tym przypadku:
- Większy plik (2812 bytes) odpowiada pełnej, zbuforowanej
  odpowiedzi HTTP z listą produktów (nagłówki + treść JSON/HTML).
- Mniejszy plik (54 bytes) odpowiada dodatkowemu wpisowi
  metadanych generowanemu przez cache_page - dotyczącemu
  nagłówka Vary (np. informacji o nagłówku Accept), potrzebnemu
  do rozróżniania różnych wersji odpowiedzi (np. HTML vs JSON)
  dla tego samego adresu URL.

Nazwy plików to hashowane wersje kluczy cache (te same klucze,
które wcześniej widzieliśmy w Django Debug Toolbar w postaci
długich napisów, np. "views.decorators.cache.cache_page...").

Wniosek

FileBasedCache przechowuje dane trwale na dysku (w plikach),
w przeciwieństwie do LocMemCache, który trzyma dane tylko
w pamięci RAM procesu i traci je przy restarcie serwera. Może to
być przydatne, gdy potrzebujemy cache przetrwać restart aplikacji,
choć jest wolniejszy niż cache w pamięci.
"""