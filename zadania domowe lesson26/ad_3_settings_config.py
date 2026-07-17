"""
Zadanie domowe 3 - Middleware, JWT i Uwierzytelnianie w DRF
Podstawowa konfiguracja settings.py.

Fragment pliku authproject/settings.py z dodanymi wpisami
do INSTALLED_APPS oraz konfiguracją REST_FRAMEWORK i SIMPLE_JWT,
wymaganymi do obsługi uwierzytelniania przez JWT.

============================================================
1. INSTALLED_APPS - dodane aplikacje
============================================================
"""

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'djoser',
]


"""
============================================================
2. REST_FRAMEWORK - domyślne uwierzytelnianie przez JWT
============================================================
"""

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}


"""
============================================================
3. SIMPLE_JWT - konfiguracja czasu życia tokenów
============================================================
"""

from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
} 