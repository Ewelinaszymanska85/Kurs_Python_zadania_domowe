"""
Zadanie 1 - Uruchomienie prostego kontenera i połączenie z Django (Memcached)

============================================================
KOMENDY DOCKER
============================================================

# Uruchomienie kontenera Memcached w tle, z przekierowaniem
# domyślnego portu 11211
docker run -d -p 11211:11211 --name lesson32_memcached memcached

# Weryfikacja, że kontener działa
docker ps

============================================================
INSTALACJA KLIENTA PYTHONA
============================================================

pip install pymemcache

============================================================
KONFIGURACJA (config/settings.py) - fragment dodany
============================================================
"""

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        "LOCATION": "127.0.0.1:11211",
    }
}

"""
============================================================
WERYFIKACJA (Django shell)
============================================================

python manage.py shell

>>> from django.core.cache import cache
>>> cache.set("test_key", "Działa!", timeout=30)
>>> cache.get("test_key")
'Działa!'

============================================================
WNIOSEK
============================================================

Django (uruchomione lokalnie, poza kontenerem na tym etapie)
poprawnie łączy się z Memcached działającym w osobnym
kontenerze Docker, dostępnym przez port 11211 przekierowany
na hosta. To pokazuje podstawowy wzorzec integracji aplikacji
Django z zewnętrzną usługą uruchomioną jako kontener - ten sam
mechanizm będzie stosowany w kolejnych zadaniach do integracji
z PostgreSQL i Redis, tylko w pełni skonteneryzowanym środowisku
(przez docker-compose), a nie jak tutaj - lokalnie + jeden
kontener.
"""