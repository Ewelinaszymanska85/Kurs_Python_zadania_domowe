# Zadanie Domowe: lekcje 35-37: Docker Compose — pełna konfiguracja z Redis, Celery workers, .env

**Kontekst:** Rozbudowa istniejącego `docker-compose.yml` projektu dyplomowego
NewsHub o wymagane elementy: własny `.env`, minimum 2 kolejki Redis, minimum
2 workery Celery, harmonogram Celery Beat.

**Pliki w tym folderze:**
- `docker-compose.yml` — finalna, kompletna konfiguracja (6 serwisów)
- `.env.example` — wzór pliku zmiennych środowiskowych (bez prawdziwych
  sekretów; w projekcie plik `.env` jest w `.gitignore`, więc nie trafia do
  repozytorium)
- `settings_fragment.py` — fragmenty `core/settings.py` zmienione na potrzeby
  tego zadania

---

## Wymagania zadania i jak zostały spełnione

### 1. Baza danych na kontenerze
Serwis `db` — obraz `postgres:16`, dane trwałe przez named volume
`postgres_data`, konfiguracja (nazwa bazy, użytkownik, hasło) pobierana
z `.env` przez `${DB_NAME}`, `${DB_USER}`, `${DB_PASSWORD}`.

### 2. Django-app na kontenerze
Serwis `web` — własny `Dockerfile`, uruchamiany produkcyjnym serwerem
Gunicorn (`gunicorn core.wsgi:application --workers 3`), nie developerskim
`runserver`.

### 3. Pełna konfiguracja
Wszystkie serwisy (`db`, `web`, `celery_worker_default`, `celery_worker_rss`,
`celery_beat`) korzystają z tego samego obrazu Docker (poza `redis`, który
używa oficjalnego obrazu `redis:7-alpine`), mają zdefiniowane `depends_on`
zapewniające poprawną kolejność startu, oraz osobny wolumen dla trwałości
danych PostgreSQL.

### 4. Własny .env
Wcześniej wszystkie dane (klucz sekretny, dane logowania do bazy, host Redis)
były wpisane na sztywno w `docker-compose.yml` i `settings.py`. Zmieniono to:

- utworzono plik `.env` z sekretami (Django `SECRET_KEY`, dane PostgreSQL,
  host Redis)
- `settings.py` czyta te wartości przez `os.environ.get(...)`, z bezpiecznymi
  wartościami domyślnymi (dla uruchomienia lokalnego, bez Dockera)
- każdy serwis w `docker-compose.yml` wczytuje `.env` przez `env_file:`,
  zamiast duplikować zmienne w każdej sekcji `environment:` osobno
- `.env` jest w `.gitignore` — sekrety nie trafiają do repozytorium

### 5. Redis (min. 2 kolejki)
Jeden kontener Redis (`redis:7-alpine`), pełniący podwójną rolę: broker
wiadomości dla Celery (baza logiczna `/0`) oraz backend cache Django
(baza logiczna `/1`, konfiguracja w `settings.py`, poza zakresem tego
konkretnego zadania).

Skonfigurowano **dwie kolejki zadań** przez `CELERY_TASK_ROUTES`:
```python
CELERY_TASK_ROUTES = {
    'sources.tasks.*': {'queue': 'rss'},
}
CELERY_TASK_DEFAULT_QUEUE = 'default'
```
Zadania pobierania RSS (`sources.tasks.fetch_feed`,
`sources.tasks.fetch_all_active_feeds`) trafiają do dedykowanej kolejki
`rss`. Wszystkie pozostałe (przyszłe) zadania domyślnie trafiają do
kolejki `default`. Rozdzielenie kolejek zapobiega sytuacji, w której wolne
zadania pobierania zewnętrznych kanałów RSS blokowałyby inne, potencjalnie
pilniejsze zadania w tle.

### 6. Celery workers (min. 2)
Dwa osobne serwisy, każdy nasłuchujący innej kolejki:

```yaml
celery_worker_default:
  command: celery -A core worker -l INFO -Q default -n worker_default@%h

celery_worker_rss:
  command: celery -A core worker -l INFO -Q rss -n worker_rss@%h
```

Zweryfikowano w logach obu workerów (`docker compose logs celery_worker_rss`
/ `celery_worker_default`), że każdy z nich faktycznie nasłuchuje wyłącznie
przypisanej mu kolejki, i że zadania RSS są odbierane i wykonywane
**wyłącznie** przez `worker_rss`.

### 7. Celery Beat (harmonogram)
Serwis `celery_beat` uruchamia zadanie `fetch_all_active_feeds` cyklicznie,
zgodnie z `CELERY_BEAT_SCHEDULE` (`crontab(minute='*/30')` — co 30 minut).
Zweryfikowane działanie: po starcie kontenerów, Beat automatycznie wywołał
zadanie bez żadnej ręcznej ingerencji.

---

## Weryfikacja końcowa

```bash
docker compose down --remove-orphans
docker compose up -d --build
docker compose ps                              # 6 kontenerów: db, redis, web,
                                                 # celery_worker_default,
                                                 # celery_worker_rss, celery_beat
docker compose exec web python manage.py migrate
docker compose logs celery_worker_rss --tail 20     # potwierdza: [queues] .> rss
docker compose logs celery_worker_default --tail 15  # potwierdza: [queues] .> default
docker compose exec web python manage.py test        # 38/38 testów przechodzi
```

Wynik: pełna, poprawnie skonfigurowana architektura wielokontenerowa z
rozdzielonymi kolejkami zadań, zweryfikowana zarówno przez logi Celery, jak
i przez pełny zestaw testów automatycznych — reorganizacja infrastruktury nie
naruszyła żadnej funkcjonalności aplikacji.