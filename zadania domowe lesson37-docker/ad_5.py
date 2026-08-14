"""
Środowisko wielokontenerowe (Django + PostgreSQL + Redis)

Kompletne rozwiązanie obejmuje: docker-compose.yml, zmiany w
settings.py, plik .env oraz wyniki testów trwałości danych.

============================================================
1. DOCKER-COMPOSE.YML (już istniejący, poprawny)
============================================================

services:
  backend:
    build: .
    container_name: django_docker_demo_backend
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - database
      - redis
    networks:
      - demo_network

  database:
    image: postgres:16-alpine
    container_name: django_docker_demo_postgres
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - demo_network

  redis:
    image: redis:7-alpine
    container_name: django_docker_demo_redis
    networks:
      - demo_network

networks:
  demo_network:
    driver: bridge

volumes:
  postgres_data:

============================================================
2. SETTINGS.PY - poprawka sekcji DATABASES
============================================================

Przed poprawką ENGINE błędnie wskazywał na sqlite3, mimo że
reszta konfiguracji (USER, PASSWORD, HOST, PORT) była już
przygotowana pod PostgreSQL.
"""

import os

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.getenv('DB_NAME', 'lesson32_db'),
        'USER': os.getenv('DB_USER', 'lesson32_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'lesson32_pass'),
        'HOST': os.getenv('DB_HOST', 'database'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

"""
============================================================
3. .ENV (już istniejący, poprawny)
============================================================

DEBUG=1
SECRET_KEY=moj-tajny-klucz-do-zadania-2
DB_ENGINE=django.db.backends.postgresql
DB_NAME=lesson32_db
DB_USER=lesson32_user
DB_PASSWORD=lesson32_pass
DB_HOST=database
DB_PORT=5432
REDIS_URL=redis://redis:6379/1

============================================================
4. KOMENDY UŻYTE DO WYKONANIA ZADANIA
============================================================

# Uruchomienie wszystkich kontenerów
docker compose up -d --build

# Sprawdzenie statusu
docker compose ps

# Migracje z wnętrza kontenera backend
docker compose exec backend python manage.py migrate

# Utworzenie superusera z wnętrza kontenera
docker compose exec backend python manage.py createsuperuser

# Test trwałości danych - usunięcie kontenerów (BEZ flagi -v,
# żeby zachować wolumen postgres_data)
docker compose down

# Ponowne utworzenie kontenerów
docker compose up -d --build

============================================================
5. WYNIKI TESTU TRWAŁOŚCI DANYCH
============================================================

1. Utworzono superusera wewnątrz kontenera backend.
2. Zalogowano się poprawnie do panelu admina (http://localhost:8000/admin/).
3. Wykonano `docker compose down` (usunięcie kontenerów, ale
   NIE wolumenów).
4. Wykonano `docker compose up -d --build` (ponowne utworzenie
   kontenerów od zera).
5. Wylogowano się z panelu admina i zalogowano ponownie, ręcznie
   wpisując te same dane logowania.
6. Logowanie powiodło się - potwierdza to, że dane superusera
   PRZETRWAŁY usunięcie i odtworzenie kontenera PostgreSQL,
   dzięki named volume "postgres_data".

Wniosek

Kluczowa zasada Dockera: kontenery są ulotne (ephemeral), ale
NAMED VOLUMES żyją niezależnie od cyklu życia kontenerów. Dopóki
wolumen nie zostanie jawnie usunięty (np. przez `docker compose
down -v` lub `docker volume rm`), dane w nim zapisane przetrwają
dowolną liczbę usunięć i odtworzeń kontenera, który go używa.
Dzięki nazwie usługi "database" (Docker DNS) oraz zmiennym
środowiskowym z pliku .env, konfiguracja połączenia Django-Postgres
pozostaje spójna niezależnie od tego, ile razy kontenery zostaną
zrestartowane.
"""