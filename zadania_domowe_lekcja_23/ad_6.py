"""
Zadanie domowe 6 - Panel administracyjny Django
Pole generowane dynamicznie - niestandardowa metoda w list_display.

Stworzenie w CarAdmin metody, która łączy markę
i model samochodu w jeden czytelny string, wyświetlany jako
dodatkowa kolumna na liście w panelu admina.
"""

from django.contrib import admin
from proj.cars.models import Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    """
    Klasa konfiguracyjna panelu admina dla modelu Car
    z dodatkową, dynamicznie generowaną kolumną "Pełna nazwa".
    """

    list_display = ('full_name', 'year', 'is_available')

    def full_name(self, obj):
        """
        Łączy markę i model samochodu w jeden string.

        Args:
            obj (Car): Instancja samochodu przekazywana automatycznie
                       przez Django dla każdego wiersza listy.

        Returns:
            str: Połączona marka i model, np. "Ford Mustang".
        """
        return f"{obj.brand} {obj.model}"

    # Nagłówek kolumny wyświetlany w panelu admina zamiast nazwy metody
    full_name.short_description = "Pełna nazwa" 