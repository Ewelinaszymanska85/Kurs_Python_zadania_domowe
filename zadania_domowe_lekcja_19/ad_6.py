# =============================================================================
# ZADANIE 6: Definicja modelu
# =============================================================================


# -----------------------------------------------------------------------------
# ogloszenia/models.py
# -----------------------------------------------------------------------------
from django.db import models


class Ogloszenie(models.Model):
    tytul = models.CharField(max_length=100)
    opis = models.TextField()
    cena = models.DecimalField(max_digits=8, decimal_places=2)
    data_dodania = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tytul


# Komendy wykonane po zdefiniowaniu modelu:
#
#     python manage.py makemigrations
#
# Efekt:
#     Migrations for 'ogloszenia':
#       ogloszenia\migrations\0001_initial.py
#         + Create model Ogloszenie
#
#     python manage.py migrate
#
# Efekt:
#     Applying ogloszenia.0001_initial... OK 