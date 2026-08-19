# ============================================================
# Zadanie 8 - Połącz modele relacją
# ============================================================


# ------------------------------------------------------------
# le20/pages/models.py
# (CAŁY PLIK - zaktualizowana wersja, dokładnie pod Twój realny kod)
# ------------------------------------------------------------
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
    )

    def __str__(self):
        return self.name


class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title


# ------------------------------------------------------------
# Konsola (z głównego katalogu projektu, gdzie jest manage.py)
# Wygenerowanie i wykonanie migracji po zmianie modelu
# ------------------------------------------------------------
# python manage.py makemigrations
#
# Django zapyta o wartość domyślną dla nowego, wymaganego pola
# 'category' (bo migracje zakładają, że mogą już istnieć rekordy
# Product, nawet jeśli baza jest pusta):
#
#   It is impossible to add a non-nullable field 'category' to
#   product without specifying a default.
#   Please select a fix:
#    1) Provide a one-off default now (...)
#    2) Quit and manually define a default value in models.py.
#
# Wybierz opcję 1, a jako wartość wpisz 1:
#
#   Select an option: 1
#   >>> 1
#
# Efekt:
#   Migrations for 'pages':
#     pages\migrations\0003_category_product_category.py
#       + Create model Category
#       + Add field category to product
#
# Następnie zastosuj migrację:
#
# python manage.py migrate
#
# Efekt:
#   Applying pages.0003_category_product_category... OK