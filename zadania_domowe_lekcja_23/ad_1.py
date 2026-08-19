"""
Zadanie domowe 1 - Panel administracyjny Django
Podstawowa rejestracja modelu Car w panelu admina.

Plik demonstruje najprostszy sposób udostępnienia modelu
w panelu administracyjnym - bez dodatkowej konfiguracji wyświetlania.
"""

from django.contrib import admin
from proj.cars.models import Car

# Rejestracja modelu Car w panelu admina - wersja podstawowa
admin.site.register(Car) 