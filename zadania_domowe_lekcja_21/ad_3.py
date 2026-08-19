# ============================================================
# Lekcja 21 - Zadanie 3 - Podstawowy widok i szablon (kategorie)
# ============================================================


# ------------------------------------------------------------
# articles/views.py
# (CAŁY PLIK - zastąp obecną, pustą zawartość tą wersją)
# ------------------------------------------------------------
from django.shortcuts import render
from .models import Category


def category_list_view(request):
    """
    Widok wyświetlający listę wszystkich kategorii zapisanych w bazie danych.
    """
    categories = Category.objects.all()

    context = {
        "categories": categories,
    }

    return render(request, "articles/category_list.html", context)


# ------------------------------------------------------------
# articles/urls.py
# (NOWY plik - stwórz go w folderze articles/, obok views.py)
# ------------------------------------------------------------
from django.urls import path
from .views import category_list_view

urlpatterns = [
    path("categories/", category_list_view, name="category-list"),
]


# ------------------------------------------------------------
# le21/urls.py
# (CAŁY PLIK - zastąp obecną zawartość tą wersją; dodany import
#  include oraz nowa ścieżka do articles.urls)
# ------------------------------------------------------------
"""
URL configuration for le21 project.
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('articles.urls')),
] 