"""
Zadanie domowe 2 - Cache w Django REST Framework
Instalacja Django Debug Toolbar.

Kompletne rozwiązanie zadania obejmuje 4 elementy konfiguracji
w cacheproject/settings.py oraz jedną zmianę w urls.py.

============================================================
1. INSTALLED_APPS - dodana aplikacja
============================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'products',
    'debug_toolbar',
]

============================================================
2. MIDDLEWARE - dodane, jak najwyżej (po SecurityMiddleware)
============================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

============================================================
3. INTERNAL_IPS - wymagane, żeby toolbar się wyświetlał
============================================================

INTERNAL_IPS = [
    '127.0.0.1',
]

============================================================
4. URLS (cacheproject/urls.py) - fragment do dodania
============================================================
"""

from django.urls import path, include

urlpatterns_fragment = [
    path('__debug__/', include('debug_toolbar.urls')),
]

"""
============================================================
WERYFIKACJA
============================================================

Po wejściu na http://127.0.0.1:8000/api/products/ panel Django
Debug Toolbar pojawił się po prawej stronie ekranu. Zakładka
"Cache" pokazuje podsumowanie operacji:

Total calls: 0
Total time: 0.00 ms
Cache hits: 0
Cache misses: 0

Wynik jest zgodny z oczekiwaniami - żaden widok nie korzystał
jeszcze z cache, więc licznik jest zerowy.
"""