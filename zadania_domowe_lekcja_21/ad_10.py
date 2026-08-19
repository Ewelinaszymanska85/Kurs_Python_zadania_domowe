# ============================================================
# Lekcja 21 - Zadanie 10 - Prosty formularz wyszukiwania
# ============================================================


# ------------------------------------------------------------
# articles/views.py
# (CAŁY PLIK - zastąp obecną zawartość tą wersją;
#  category_list_view i category_detail_view bez zmian,
#  article_list_view rozszerzony o obsługę parametru ?q=)
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
    Widok wyświetlający listę wszystkich OPUBLIKOWANYCH artykułów,
    z możliwością wyszukiwania po tytule przez parametr GET 'q'
    (np. /articles/?q=sport).

    Dla każdego artykułu dodajemy w Pythonie dodatkową, tymczasową
    flagę `is_new` (artykuł opublikowany w ciągu ostatnich 3 dni).
    """
    published_articles = Article.objects.filter(is_published=True)

    search_query = request.GET.get('q')

    if search_query:
        published_articles = published_articles.filter(
            title__icontains=search_query
        )

    three_days_ago = timezone.now() - timedelta(days=3)

    for article in published_articles:
        article.is_new = article.pub_date >= three_days_ago

    context = {
        "articles": published_articles,
        "search_query": search_query or "",
    }

    return render(request, "articles/article_list.html", context) 