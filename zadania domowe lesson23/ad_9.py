"""
Zadanie domowe 9 - Panel administracyjny Django
Wyświetlanie miniaturki zdjęcia w liście - format_html.

Dodanie do CarAdmin metody, która renderuje
miniaturkę zdjęcia samochodu bezpośrednio na liście w panelu admina,
z bezpiecznym generowaniem HTML za pomocą format_html.
"""

from django.contrib import admin 
from django.utils.html import format_html
from proj.cars.models import Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    """
    Klasa konfiguracyjna panelu admina dla modelu Car
    z miniaturką zdjęcia widoczną na liście.
    """

    list_display = ('brand', 'model', 'year', 'is_available', 'photo_thumbnail')

    def photo_thumbnail(self, obj):
        """
        Renderuje miniaturkę zdjęcia samochodu na liście w panelu admina.

        Używa format_html zamiast zwykłego formatowania stringów,
        żeby uniknąć podatności XSS - format_html automatycznie
        ucieka (escape'uje) niebezpieczne znaki w danych, które
        nie są jawnie oznaczone jako bezpieczny HTML.

        Args:
            obj (Car): Instancja samochodu przekazywana automatycznie
                       przez Django dla każdego wiersza listy.

        Returns:
            str: Znacznik <img> ze zdjęciem samochodu, albo tekst
                 informujący o braku zdjęcia.
        """
        if obj.photo:
            return format_html(
                '<img src="{}" width="150" />',
                obj.photo.url 
            )
        return "Brak zdjęcia"

    # Nagłówek kolumny wyświetlany w panelu admina zamiast nazwy metody
    photo_thumbnail.short_description = "Miniaturka"