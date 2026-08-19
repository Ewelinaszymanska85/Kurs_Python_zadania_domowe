# =============================================================================
# ZADANIE 4: Konfiguracja bazy danych
# =============================================================================


# -----------------------------------------------------------------------------
# mojastrona/settings.py  (fragment - sekcja DATABASES)
# -----------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mojastrona_db',
        'USER': 'mojastrona_user',
        'PASSWORD': 'fikcyjne_haslo123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}