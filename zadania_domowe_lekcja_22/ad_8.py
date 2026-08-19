# ============================================================
# Lekcja 22 - Zadanie 8 - Normalizacja Postów (Tagi)
# ============================================================


# ------------------------------------------------------------
# blog/models.py
# (CAŁY PLIK - zastąp obecną zawartość tą wersją)
#
# Nowość: model Tag oraz pole `tags` w modelu Post.
#
# Dlaczego ManyToManyField, a nie ForeignKey?
# - ForeignKey (użyty przy Category) to relacja "wiele do jednego":
#   jeden post ma DOKŁADNIE JEDNĄ kategorię, ale kategoria może mieć
#   wiele postów.
# - ManyToManyField to relacja "wiele do wielu": jeden post może mieć
#   WIELE tagów jednocześnie, a jeden tag może być przypisany
#   do WIELU postów. Dokładnie taka zależność jest potrzebna przy
#   tagach (np. post może być jednocześnie otagowany "Python" i
#   "Django", a tag "Python" może występować pod wieloma postami).
#
# Django "pod maską" tworzy dla ManyToManyField dodatkową,
# ukrytą tabelę pośredniczącą w bazie danych, która przechowuje
# pary (post_id, tag_id) - to standardowy sposób implementacji
# relacji wiele-do-wielu w bazach relacyjnych.
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


class Tag(models.Model):
    """
    Model reprezentujący pojedynczy tag, którym można oznaczyć post
    (np. 'Python', 'Django', 'Backend').

    Jeden tag może być przypisany do wielu postów jednocześnie -
    relacja jest zdefiniowana po stronie modelu Post (pole `tags`).
    """

    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Nazwa tagu",
    )

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tagi"
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
    # ManyToManyField - relacja wiele-do-wielu z modelem Tag.
    # blank=True oznacza, że post NIE MUSI mieć żadnego tagu
    # (pole nie jest wymagane, np. w formularzach/panelu admina).
    tags = models.ManyToManyField(
        Tag,
        related_name="posts",
        blank=True,
        verbose_name="Tagi",
    )

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posty"
        ordering = ["-publication_date"]

    def __str__(self):
        return self.title


# ------------------------------------------------------------
# Konsola (z głównego katalogu projektu, gdzie jest manage.py)
# ------------------------------------------------------------
# python manage.py makemigrations
# python manage.py migrate
#
# Django wygeneruje migrację, która:
# 1. Tworzy nową tabelę dla modelu Tag,
# 2. Tworzy dodatkową, ukrytą tabelę pośredniczącą łączącą
#    posty z tagami (relacja wiele-do-wielu). 