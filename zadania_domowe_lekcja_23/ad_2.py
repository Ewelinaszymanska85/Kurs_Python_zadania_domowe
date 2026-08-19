"""
Zadanie domowe 2 - Panel administracyjny Django
Konfiguracja panelu admina dla modelu Car.

Plik demonstruje rejestrację modelu w panelu administracyjnym
oraz dostosowanie sposobu wyświetlania listy rekordów.
"""

from django.contrib import admin
from proj.cars.models import Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    """
    Klasa konfiguracyjna panelu admina dla modelu Car.

    Dzięki niej lista samochodów w panelu admina wyświetla
    wybrane kolumny zamiast domyślnej reprezentacji __str__.
    """

    # Kolumny widoczne na liście rekordów w panelu admina
    list_display = ('brand', 'model', 'year', 'is_available')

    # Możliwość filtrowania listy po dostępności i roku produkcji
    list_filter = ('is_available', 'year')

    # Pole wyszukiwania - umożliwia szybkie znalezienie samochodu po marce lub modelu
    search_fields = ('brand', 'model')

    # Domyślne sortowanie listy - najnowsze roczniki na górze
    ordering = ('-year',) 