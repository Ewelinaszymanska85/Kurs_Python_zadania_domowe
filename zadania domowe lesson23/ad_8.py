"""
Zadanie domowe 8 - Panel administracyjny Django
Własna akcja administracyjna - mark_as_unavailable.

Stworzenie niestandardowej akcji w panelu admina,
która pozwala hurtowo oznaczyć zaznaczone samochody jako niedostępne.
"""

from django.contrib import admin
from proj.cars.models import Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    """
    Klasa konfiguracyjna panelu admina dla modelu Car
    z niestandardową akcją hurtową.
    """

    list_display = ('brand', 'model', 'year', 'is_available')

    # Rejestracja niestandardowej akcji dostępnej w panelu admina
    actions = ['mark_as_unavailable']

    def mark_as_unavailable(self, request, queryset):
        """
        Niestandardowa akcja administracyjna.

        Ustawia pole is_available na False dla wszystkich
        zaznaczonych samochodów w panelu admina.

        Args:
            request (HttpRequest): Obiekt żądania HTTP.
            queryset (QuerySet): Zestaw zaznaczonych przez użytkownika
                                  rekordów Car, na których wykonywana
                                  jest akcja.
        """
        # update() na queryset jest wydajniejsze niż pętla po obiektach,
        # bo generuje jedno zapytanie SQL zamiast wielu
        updated_count = queryset.update(is_available=False)

        # Komunikat informacyjny wyświetlany użytkownikowi po wykonaniu akcji
        self.message_user(
            request,
            f"Oznaczono {updated_count} samochód(ów) jako niedostępne."
        )

    # Nazwa akcji widoczna w rozwijanej liście w panelu admina
    mark_as_unavailable.short_description = "Oznacz jako niedostępne"