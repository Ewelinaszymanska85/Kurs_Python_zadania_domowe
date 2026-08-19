# ============================================================
# Lekcja 22 - Zadanie 1 - Normalizacja Postów (Kategorie)
# ============================================================


# ------------------------------------------------------------
# blog/models.py
# (CAŁY PLIK - zastąp obecną, domyślną zawartość tą wersją)
# ------------------------------------------------------------
from django.db import models


class Category(models.Model):
    """
    Model reprezentujący kategorię, do której mogą być
    przypisywane posty bloga (np. 'Technologia', 'Podróże', 'Kulinaria').
    """

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nazwa kategorii",
    )

    class Meta:
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    Model reprezentujący pojedynczy post na blogu.
    """

    title = models.CharField(max_length=200, verbose_name="Tytuł")
    content = models.TextField(verbose_name="Treść")
    publication_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data publikacji",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Kategoria",
    )

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posty"
        ordering = ["-publication_date"]

    def __str__(self):
        return self.title


# ------------------------------------------------------------
# Konsola (z głównego katalogu projektu, gdzie jest manage.py)
# Wygenerowanie i wykonanie migracji po stworzeniu nowych modeli
# ------------------------------------------------------------
# python manage.py makemigrations
# python manage.py migrate
#
# To pierwsze migracje dla aplikacji blog (baza jest pusta),
# więc powinno przejść bez żadnych dodatkowych pytań.