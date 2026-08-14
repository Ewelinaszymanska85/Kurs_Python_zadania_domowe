"""
Zadanie 2 - Własny Dockerfile dla aplikacji Django

============================================================
DOCKERFILE (plik "Dockerfile" w głównym katalogu projektu)
============================================================

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

============================================================
ZMIENNE ŚRODOWISKOWE (.env)
============================================================

DEBUG=1
SECRET_KEY=moj-tajny-klucz-do-zadania-2

============================================================
KONFIGURACJA (config/settings.py) - fragment zmieniony
============================================================
"""

import os

SECRET_KEY = os.getenv('SECRET_KEY', 'domyslny-klucz-insecure')
DEBUG = int(os.getenv('DEBUG', 1))
ALLOWED_HOSTS = ['*']

"""
============================================================
KOMENDY DOCKER
============================================================

# Zbudowanie obrazu
docker build -t django-docker-demo:v1 .

# Uruchomienie kontenera z wczytaniem zmiennych z .env
docker run -d -p 8000:8000 --env-file .env --name django_docker_demo_container django-docker-demo:v1

# Weryfikacja
curl -UseBasicParsing http://localhost:8000/health/

============================================================
NAPOTKANA TRUDNOŚĆ
============================================================

Po pierwszej próbie uruchomienia kontenera, endpoint /health/ nie
odpowiadał ("nie można połączyć się z serwerem"). Sprawdzenie logów
kontenera (docker logs django_docker_demo_container) ujawniło
prawdziwą przyczynę:

    NameError: name 'os' is not defined. Did you forget to import 'os'?

Mimo dodania linii `SECRET_KEY = os.getenv(...)`, brakowało importu
`import os` na samej górze pliku settings.py - Python nie wie, czym
jest "os", dopóki nie zostanie on jawnie zaimportowany. Po dodaniu
`import os` na górze pliku, przebudowaniu obrazu (docker build) i
ponownym uruchomieniu kontenera, wszystko zadziałało poprawnie.

============================================================
WNIOSEK
============================================================

Ten epizod dobrze pokazuje, dlaczego sprawdzanie logów kontenera
(docker logs) jest kluczowym narzędziem debugowania w Dockerze -
kontener "milczący" (brak odpowiedzi na porcie) w rzeczywistości
crashuje przy starcie z powodu błędu w kodzie Pythona, a nie
z powodu problemu z siecią czy konfiguracją Dockera samą w sobie.
"""