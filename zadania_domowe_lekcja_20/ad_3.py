# =============================================================================
# ZADANIE 3: Stwórz prosty model
# =============================================================================


# -----------------------------------------------------------------------------
# pages/models.py
# -----------------------------------------------------------------------------
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name


# Komendy wykonane po zdefiniowaniu modelu:
#
#     python manage.py makemigrations
#     python manage.py migrate
#
# Efekt: migracje wykonane poprawnie, bez błędów. Tabela "pages_product"
# została utworzona w bazie danych.