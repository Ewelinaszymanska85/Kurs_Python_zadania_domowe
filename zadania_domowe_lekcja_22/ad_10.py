# ============================================================
# Lekcja 22 - Zadanie 10 - Rejestracja i Logowanie (django-allauth)
# ============================================================
#
# django-allauth to zewnętrzna aplikacja Django, która "z pudełka"
# dostarcza gotowe widoki, formularze i szablony do rejestracji,
# logowania, wylogowania, resetowania hasła itd. Zamiast pisać to
# wszystko samodzielnie od zera, korzystamy z gotowego, sprawdzonego
# rozwiązania - to jest dokładnie ten temat z punktu 5 lekcji
# ("Moduły / Aplikacje Zewnętrzne w Django").
#
# Konfiguracja przebiega w 3 standardowych krokach (patrz materiał
# z lekcji, punkt 5):
# 1. Instalacja paczki przez pip.
# 2. Dodanie aplikacji do INSTALLED_APPS w settings.py + dodatkowa
#    konfiguracja wymagana przez allauth.
# 3. Podpięcie URL-i allauth w urls.py.
# ============================================================


# ------------------------------------------------------------
# Krok 1: Konsola - instalacja paczki
# ------------------------------------------------------------
# pip install django-allauth


# ------------------------------------------------------------
# Krok 2: le22/settings.py
# (fragmenty do DOPISANIA / ZMIANY w istniejącym pliku - NIE
#  zastępuj całego pliku, tylko dodaj poniższe elementy w
#  odpowiednich miejscach)
# ------------------------------------------------------------

# --- 2a. INSTALLED_APPS ---
# Znajdź listę INSTALLED_APPS i dodaj do niej poniższe wpisy
# (jeśli jakiegoś z nich już tam nie ma):
#
# INSTALLED_APPS = [
#     "django.contrib.admin",
#     "django.contrib.auth",
#     "django.contrib.contenttypes",
#     "django.contrib.sessions",
#     "django.contrib.messages",
#     "django.contrib.staticfiles",
#     "django.contrib.sites",            # <-- WYMAGANE przez allauth
#     "allauth",                          # <-- NOWE
#     "allauth.account",                  # <-- NOWE
#     "blog",
# ]

# --- 2b. SITE_ID ---
# django.contrib.sites wymaga zdefiniowania ID strony.
# Dopisz na końcu pliku settings.py:
#
# SITE_ID = 1

# --- 2c. MIDDLEWARE ---
# Nowsze wersje django-allauth (65.x) wymagają dodania własnego
# middleware. Bez tego kroku pojawi się błąd:
# "ImproperlyConfigured: allauth.account.middleware.AccountMiddleware
#  must be added to settings.MIDDLEWARE"
#
# Znajdź listę MIDDLEWARE i dodaj na końcu nową linijkę:
#
# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
#     'allauth.account.middleware.AccountMiddleware',   # <-- NOWE
# ]

# --- 2d. AUTHENTICATION_BACKENDS ---
# allauth potrzebuje własnego backendu uwierzytelniania,
# obok domyślnego backendu Django. Dopisz:
#
# AUTHENTICATION_BACKENDS = [
#     "django.contrib.auth.backends.ModelBackend",
#     "allauth.account.auth_backends.AuthenticationBackend",
# ]

# --- 2d. Ustawienia allauth (uproszczone, na potrzeby nauki) ---
# Dopisz poniższe ustawienia, żeby uprościć proces rejestracji
# (bez wymogu potwierdzania e-maila, co ułatwia testowanie lokalnie):
#
# ACCOUNT_EMAIL_VERIFICATION = "none"
# LOGIN_REDIRECT_URL = "/"
# ACCOUNT_LOGOUT_REDIRECT_URL = "/"


# ------------------------------------------------------------
# Krok 3: le22/urls.py
# (CAŁY PLIK - zastąp obecną zawartość tą wersją; dodana nowa
#  ścieżka "accounts/", pod którą allauth udostępnia WSZYSTKIE
#  swoje widoki: logowanie, rejestrację, wylogowanie itd.)
# ------------------------------------------------------------
"""
URL configuration for le22 project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('blog.urls')),
]


# ------------------------------------------------------------
# Krok 4: Konsola - migracje
# ------------------------------------------------------------
# allauth i django.contrib.sites dodają własne modele do bazy
# danych (np. tabelę Site), dlatego trzeba zaaplikować ich migracje:
#
# python manage.py migrate


# ------------------------------------------------------------
# Krok 5: Testowanie w przeglądarce
# ------------------------------------------------------------
# Po uruchomieniu serwera (python manage.py runserver) dostępne
# są m.in. następujące adresy dostarczone przez allauth:
#
# http://127.0.0.1:8000/accounts/signup/  -> formularz rejestracji
# http://127.0.0.1:8000/accounts/login/   -> formularz logowania
# http://127.0.0.1:8000/accounts/logout/  -> wylogowanie 