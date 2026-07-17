"""
Zadanie domowe 1 - Cache w Django REST Framework
Konfiguracja locmem cache.

Fragment pliku cacheproject/settings.py z konfiguracją domyślnego
cache, wykorzystującego LocMemCache - pamięć podręczną przechowywaną
lokalnie w procesie Pythona. Jest to najprostszy backend cache,
idealny do celów deweloperskich.
"""

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

"""
Weryfikacja

Po dodaniu tej konfiguracji do settings.py i uruchomieniu serwera
(python manage.py runserver), aplikacja startuje bez błędów, co
potwierdza poprawną konfigurację cache.
"""