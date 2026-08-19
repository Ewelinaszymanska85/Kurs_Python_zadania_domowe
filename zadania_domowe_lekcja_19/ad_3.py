# =============================================================================
# ZADANIE 3: Tworzenie aplikacji
# =============================================================================

# Komenda wykonana w konsoli (w katalogu mojastrona_projekt):
#
#     python manage.py startapp ogloszenia
#
# Efekt: stworzony nowy folder "ogloszenia" z plikami:
#     ogloszenia/
#     ├── migrations/
#     ├── __init__.py
#     ├── admin.py
#     ├── apps.py
#     ├── models.py
#     ├── tests.py
#     └── views.py


# -----------------------------------------------------------------------------
# mojastrona/settings.py  (fragment - sekcja INSTALLED_APPS)
# -----------------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ogloszenia',
] 