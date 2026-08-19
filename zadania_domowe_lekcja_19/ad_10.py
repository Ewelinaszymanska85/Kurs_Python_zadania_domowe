# =============================================================================
# ZADANIE 10: Personalizacja panelu admina
# =============================================================================


# -----------------------------------------------------------------------------
# ogloszenia/models.py  (fragment - metoda __str__, dodana już w zadaniu 6)
# -----------------------------------------------------------------------------
class Ogloszenie:
    def __str__(self):
        return self.tytul


# -----------------------------------------------------------------------------
# ogloszenia/admin.py
# -----------------------------------------------------------------------------
from django.contrib import admin
from .models import Ogloszenie


class OgloszenieAdmin(admin.ModelAdmin):
    list_display = ('tytul', 'cena', 'data_dodania')


admin.site.register(Ogloszenie, OgloszenieAdmin) 