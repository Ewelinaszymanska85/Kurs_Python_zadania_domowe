# Fragment core/settings.py - zmiany wprowadzone dla zadań 35-37

# --- Baza danych: odczyt ze zmiennych środowiskowych (wcześniej na sztywno) ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'newshub'),
        'USER': os.environ.get('DB_USER', 'newshub_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'newshub_pass'),
        'HOST': os.environ.get('DATABASE_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}


# --- Celery: broker, serializacja (bez zmian względem wcześniejszej wersji) ---
CELERY_BROKER_URL = f"redis://{os.environ.get('REDIS_HOST', 'localhost')}:6379/0"
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

# --- NOWE: routing zadań do konkretnych kolejek ---
# Zadania pobierania RSS trafiają do osobnej kolejki "rss", żeby nie
# konkurowały o workera z innymi, potencjalnie szybszymi zadaniami w tle.
CELERY_TASK_ROUTES = {
    'sources.tasks.*': {'queue': 'rss'},
}

# Domyślna kolejka dla zadań bez jawnie przypisanej kolejki
CELERY_TASK_DEFAULT_QUEUE = 'default'

CELERY_BEAT_SCHEDULE = {
    'fetch-rss-every-30-min': {
        'task': 'sources.tasks.fetch_all_active_feeds',
        'schedule': crontab(minute='*/30'),
    },
} 