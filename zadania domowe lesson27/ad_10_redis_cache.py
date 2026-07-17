"""
Zadanie domowe 10 - Cache w Django REST Framework
Konfiguracja Redis jako backendu cache.

UWAGA: Zadanie udokumentowane teoretycznie. Na tym komputerze nie
jest zainstalowany Docker (ani natywny Redis dla Windows), więc
faktyczne uruchomienie serwera Redis nie zostało wykonane. Poniżej
przedstawiono kompletną, poprawną konfigurację, którą należałoby
zastosować, gdyby środowisko Redis było dostępne.

============================================================
1. INSTALACJA REDIS (przy użyciu Dockera)
============================================================

Krok 1: Zainstalować Docker Desktop (wymaga włączenia WSL2
na Windows).

Krok 2: Uruchomić kontener z Redis:

docker run -d --name redis-cache -p 6379:6379 redis

To pobierze oficjalny obraz Redis z Docker Hub i uruchomi go
w tle, udostępniając port 6379 (domyślny port Redis) na
localhost.

Krok 3: Sprawdzić, czy kontener działa:

docker ps

============================================================
2. INSTALACJA BIBLIOTEKI django-redis
============================================================

pip install django-redis

django-redis to biblioteka integrująca Redis z systemem cache
Django, zapewniająca kompatybilny backend.

============================================================
3. KONFIGURACJA CACHES (settings.py)
============================================================
"""

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

"""
Wyjaśnienie:
- 'redis://127.0.0.1:6379/1' - adres serwera Redis (host, port)
  oraz numer bazy danych Redis (Redis obsługuje wiele numerowanych
  baz w jednej instancji, tutaj używamy bazy nr 1).
- CLIENT_CLASS - klasa klienta odpowiedzialna za komunikację
  z serwerem Redis.

============================================================
4. WERYFIKACJA (jak wyglądałaby, gdyby Redis był uruchomiony)
============================================================

Po skonfigurowaniu i uruchomieniu serwera Django, każde użycie
cache (np. przez wcześniej stworzone widoki z Zadań 3, 7, 8, 9)
przekierowywałoby zapisy/odczyty do serwera Redis zamiast
LocMemCache.

W Django Debug Toolbar, zakładka "Cache" powinna pokazywać
te same informacje co przy LocMemCache (liczba wywołań, hit/miss,
czas trwania operacji), ale w kolumnie "Backend" zamiast
"default (LocMemCache)" widniałoby coś w stylu
"default (RedisCache)".

Dodatkowo, dane zapisane w Redis MOGŁYBY być sprawdzone
niezależnie od Django, np. poprzez redis-cli:

docker exec -it redis-cache redis-cli
> KEYS *
> GET <klucz_cache>

============================================================
5. RÓŻNICE WZGLĘDEM LocMemCache
============================================================

- Redis działa jako OSOBNY proces/serwer, niezależny od procesu
  Django - dane w cache są WSPÓŁDZIELONE między wieloma procesami
  serwera aplikacji (np. przy uruchomieniu Django przez Gunicorn
  z wieloma workerami), czego LocMemCache nie zapewnia (każdy
  proces ma WŁASNĄ, oddzielną pamięć podręczną).
- Dane w Redis przetrwają restart aplikacji Django (o ile sam
  serwer Redis pozostaje uruchomiony), podobnie jak przy
  FileBasedCache, ale ze znacznie lepszą wydajnością.
- Redis to standardowy wybór dla środowisk produkcyjnych, ze
  względu na szybkość, skalowalność i dodatkowe funkcje
  (np. automatyczne wygasanie kluczy, struktury danych takie
  jak listy czy zbiory).

Wniosek

Konfiguracja Redis jako backendu cache w Django jest stosunkowo
prosta - wymaga jedynie zmiany słownika CACHES w settings.py
i wskazania odpowiedniego adresu serwera Redis. Największym
wyzwaniem praktycznym jest samo postawienie i utrzymanie serwera
Redis (poprzez Docker lub natywną instalację), a nie integracja
z kodem Django, która pozostaje niemal identyczna jak przy innych
backendach cache.
"""