# ============================================================
# Lekcja 21 - Zadanie 8 - Logika warunkowa w szablonie
# ============================================================


# ------------------------------------------------------------
# articles/models.py
# (CAŁY PLIK - zastąp obecną zawartość tą wersją;
#  Article dostaje nowe pole is_published, Category bez zmian)
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
    is_published = models.BooleanField(
        default=True,
        verbose_name="Opublikowany",
        help_text="Czy artykuł jest widoczny publicznie na liście artykułów.",
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
# UWAGA: skoro w bazie są już 4 testowe artykuły (z zadania 7),
# Django zapyta o wartość domyślną dla nowego pola is_published.
# To jednak pole BooleanField z default=True - mimo to Django
# i tak pyta przy makemigrations (taka jest jego natura przy
# dodawaniu nowego pola do istniejącego modelu z danymi).
# Wybierz opcję 1, a jako wartość wpisz: True


# ------------------------------------------------------------
# articles/views.py
# (CAŁY PLIK - zastąp obecną zawartość tą wersją;
#  dodany import timedelta, timezone oraz nowy widok
#  article_list_view z logiką "NOWOŚĆ!")
# ------------------------------------------------------------
from datetime import timedelta

from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Category, Article


def category_list_view(request):
    """
    Widok wyświetlający listę wszystkich kategorii zapisanych w bazie danych.
    """
    categories = Category.objects.all()

    context = {
        "categories": categories,
    }

    return render(request, "articles/category_list.html", context)


def category_detail_view(request, pk):
    """
    Widok wyświetlający szczegóły jednej, konkretnej kategorii
    na podstawie jej ID (pk) przekazanego w adresie URL.

    Jeśli kategoria o podanym ID nie istnieje, Django automatycznie
    wyświetli stronę błędu 404 (dzięki get_object_or_404).
    """
    category = get_object_or_404(Category, pk=pk)

    context = {
        "category": category,
    }

    return render(request, "articles/category_detail.html", context)


def article_list_view(request):
    """
    Widok wyświetlający listę wszystkich OPUBLIKOWANYCH artykułów.

    Dla każdego artykułu dodajemy w Pythonie dodatkową, tymczasową
    flagę `is_new` (artykuł opublikowany w ciągu ostatnich 3 dni),
    żeby w szablonie móc prosto napisać {% if article.is_new %}
    bez konieczności parsowania filtra timesince.
    """
    published_articles = Article.objects.filter(is_published=True)

    three_days_ago = timezone.now() - timedelta(days=3)

    for article in published_articles:
        article.is_new = article.pub_date >= three_days_ago

    context = {
        "articles": published_articles,
    }

    return render(request, "articles/article_list.html", context)


# ------------------------------------------------------------
# articles/urls.py
# (CAŁY PLIK - zastąp obecną zawartość tą wersją;
#  dodana nowa ścieżka articles/ dla article_list_view)
# ------------------------------------------------------------
from django.urls import path
from .views import category_list_view, category_detail_view, article_list_view

urlpatterns = [
    path("categories/", category_list_view, name="category-list"),
    path("categories/<int:pk>/", category_detail_view, name="category-detail"),
    path("articles/", article_list_view, name="article-list"),
] 