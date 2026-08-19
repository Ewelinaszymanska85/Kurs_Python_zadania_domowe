# ============================================================
# Lekcja 21 - Zadanie 7 - Relacja i wyświetlanie (część 1: model)
# ============================================================


# ------------------------------------------------------------
# articles/models.py
# (CAŁY PLIK - zastąp obecną zawartość tą wersją;
#  Article dostaje nowe pole category, Category zostaje bez zmian)
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


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="articles",
    )

    def __str__(self):
        return self.title


# ------------------------------------------------------------
# Konsola (z głównego katalogu projektu, gdzie jest manage.py)
# Wygenerowanie i wykonanie migracji po zmianie modelu
# ------------------------------------------------------------
# python manage.py makemigrations
# python manage.py migrate
#
# Baza Article jest pusta, więc migracja powinna przebiegnąć
# bez żadnych dodatkowych pytań o wartość domyślną. 