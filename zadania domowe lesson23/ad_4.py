"""
Zadanie domowe 4 - Panel administracyjny Django
Dodanie filtrów - list_filter.

Plik demonstruje dodanie do CarAdmin możliwości filtrowania
samochodów po dostępności oraz roku produkcji.
"""

from django.contrib import admin
from proj.cars.models import Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    """
    Klasa konfiguracyjna panelu admina dla modelu Car
    z możliwością filtrowania rekordów.
    """

    list_display = ('brand', 'model', 'year', 'is_available')

    # Możliwość filtrowania listy po dostępności i roku produkcji
    list_filter = ('is_available', 'year') 