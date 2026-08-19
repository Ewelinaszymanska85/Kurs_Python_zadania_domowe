"""
Zadanie domowe 7 - Panel administracyjny Django
Pole tylko do odczytu - readonly_fields.

Ustawienie pola year jako tylko do odczytu
w widoku edycji pojedynczego samochodu w panelu admina.
"""

from django.contrib import admin
from proj.cars.models import Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    """
    Klasa konfiguracyjna panelu admina dla modelu Car
    z polem year ustawionym jako tylko do odczytu.
    """

    list_display = ('brand', 'model', 'year', 'is_available')

    # Pole year będzie widoczne w formularzu edycji, ale nie będzie można go zmienić
    readonly_fields = ('year',)