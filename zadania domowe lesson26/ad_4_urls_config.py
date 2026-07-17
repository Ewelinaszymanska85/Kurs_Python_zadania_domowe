"""
Zadanie domowe 4 - Middleware, JWT i Uwierzytelnianie w DRF
Konfiguracja URLi - ścieżki Djoser.

Pełna zawartość głównego pliku authproject/urls.py z dodanymi
ścieżkami dostarczanymi przez bibliotekę Djoser, obsługującymi
rejestrację, zarządzanie użytkownikami oraz logowanie/odświeżanie
tokenów JWT.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Endpointy Djoser do zarządzania użytkownikami (m.in. /auth/users/
    # do rejestracji nowego użytkownika)
    path('auth/', include('djoser.urls')),

    # Endpointy Djoser specyficzne dla JWT (m.in. /auth/jwt/create/
    # do logowania, /auth/jwt/refresh/ do odświeżania tokenu)
    path('auth/', include('djoser.urls.jwt')),
] 