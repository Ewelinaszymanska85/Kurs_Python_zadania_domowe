"""
Zadanie domowe 5 - Panel administracyjny Django
Domyślne sortowanie - ordering.

Plik demonstruje ustawienie domyślnego sortowania listy samochodów
od najnowszego rocznika do najstarszego.
"""

from django.contrib import admin
from proj.cars.models import Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    """
    Klasa konfiguracyjna panelu admina dla modelu Car
    z domyślnym sortowaniem listy.
    """

    list_display = ('brand', 'model', 'year', 'is_available')

    # Domyślne sortowanie listy - najnowsze roczniki na górze
    ordering = ('-year',) 