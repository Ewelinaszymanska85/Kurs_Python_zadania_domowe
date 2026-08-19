# ============================================================
# Lekcja 21 - Zadanie 1 - Nowy model (Category)
# ============================================================


# ------------------------------------------------------------
# le21/articles/models.py
# (dopisać na końcu pliku, obok istniejącego modelu Article)
# ------------------------------------------------------------
from django.db import models


class Category(models.Model):
    """
    Model reprezentujący kategorię, do której mogą być
    przypisywane artykuły (np. 'Technologia', 'Sport', 'Kultura').
    """

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nazwa kategorii",
        help_text="Unikalna nazwa kategorii (maks. 100 znaków).",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data utworzenia",
    )

    class Meta:
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"
        ordering = ["name"]

    def __str__(self):
        return self.name


# ------------------------------------------------------------
# Konsola (z głównego katalogu projektu, gdzie jest manage.py)
# Wygenerowanie i wykonanie migracji po dodaniu nowego modelu
# ------------------------------------------------------------
# python manage.py makemigrations
# python manage.py migrate
#
# Efekt (przykładowy):
#   Migrations for 'articles':
#     articles/migrations/0002_category.py
#       + Create model Category
#
#   Applying articles.0002_category... OK 