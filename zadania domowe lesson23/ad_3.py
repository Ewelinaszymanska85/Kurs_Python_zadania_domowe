"""
Zadanie domowe 3 - Panel administracyjny Django
Dodanie wyszukiwania - search_fields.

Plik demonstruje dodanie do CarAdmin możliwości wyszukiwania
samochodów po marce i modelu.
"""

from django.contrib import admin
from proj.cars.models import Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    """
    Klasa konfiguracyjna panelu admina dla modelu Car
    z możliwością wyszukiwania rekordów.
    """

    list_display = ('brand', 'model', 'year', 'is_available')

    # Pole wyszukiwania - umożliwia szybkie znalezienie samochodu po marce lub modelu
    search_fields = ('brand', 'model') 