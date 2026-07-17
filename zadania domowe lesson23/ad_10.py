"""
Zadanie domowe 10 - Panel administracyjny Django
Model powiązany i Inline - Dealer + TabularInline.

Plik demonstruje rejestrację modelu Dealer w panelu admina wraz
z wyświetlaniem przypisanych do niego samochodów bezpośrednio
na stronie edycji dealera, za pomocą TabularInline.
"""

from django.contrib import admin
from proj.cars.models import Car, Dealer


class CarInline(admin.TabularInline):
    """
    Inline pozwalający wyświetlić i edytować samochody
    przypisane do danego dealera bezpośrednio na jego stronie.

    TabularInline prezentuje powiązane rekordy w formie zwartej
    tabeli, w przeciwieństwie do StackedInline, który pokazuje
    każdy rekord jako osobny, rozbudowany formularz.
    """

    model = Car

    # Liczba pustych, dodatkowych formularzy do dodania nowego samochodu
    extra = 1

    # Ograniczenie widocznych pól w tabeli inline, żeby nie była przeładowana
    fields = ('brand', 'model', 'year', 'is_available')


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    """
    Klasa konfiguracyjna panelu admina dla modelu Dealer.

    Wyświetla listę dealerów oraz umożliwia zarządzanie
    przypisanymi do nich samochodami bezpośrednio z poziomu
    strony edycji dealera.
    """

    list_display = ('name', 'address')

    # Dołączenie inline z samochodami do widoku edycji dealera
    inlines = [CarInline]


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    """
    Klasa konfiguracyjna panelu admina dla modelu Car.
    """

    list_display = ('brand', 'model', 'year', 'is_available', 'dealer') 