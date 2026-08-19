# ============================================================
# Lekcja 22 - Zadanie 2 - Widok Kategorii
# ============================================================


# ------------------------------------------------------------
# blog/views.py
# (CAŁY PLIK - zastąp obecną, domyślną zawartość tą wersją)
# ------------------------------------------------------------
from django.shortcuts import render, get_object_or_404
from .models import Category, Post


def category_posts_view(request, category_id):
    """
    Widok wyświetlający listę wszystkich postów należących
    do danej kategorii, na podstawie jej ID przekazanego w URL-u.

    Jeśli kategoria o podanym ID nie istnieje, Django automatycznie
    wyświetli stronę błędu 404 (dzięki get_object_or_404).
    """
    category = get_object_or_404(Category, pk=category_id)
    posts = Post.objects.filter(category=category)

    context = {
        "category": category,
        "posts": posts,
    }

    return render(request, "blog/category_posts.html", context)


# ------------------------------------------------------------
# blog/urls.py
# (NOWY plik - stwórz go w folderze blog/, obok views.py)
# ------------------------------------------------------------
from django.urls import path
from .views import category_posts_view

urlpatterns = [
    path("category/<int:category_id>/", category_posts_view, name="category-posts"),
]


# ------------------------------------------------------------
# le22/urls.py
# (CAŁY PLIK - zastąp obecną zawartość tą wersją; dodany import
#  include oraz nowa ścieżka do blog.urls)
# ------------------------------------------------------------
"""
URL configuration for le22 project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
] 