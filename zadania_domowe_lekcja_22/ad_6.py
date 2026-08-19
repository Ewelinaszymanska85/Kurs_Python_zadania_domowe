# ============================================================
# Lekcja 22 - Zadanie 6 - Wyszukiwarka Postów
# ============================================================


# ------------------------------------------------------------
# blog/views.py
# (CAŁY PLIK - zastąp obecną zawartość tą wersją)
#
# Zmiana dotyczy funkcji home_view:
# - odbieramy frazę szukaną z parametru GET o nazwie "q"
#   (np. adres: /?q=django)
# - jeśli fraza została podana, filtrujemy posty, których TYTUŁ
#   LUB TREŚĆ zawiera tę frazę (bez rozróżniania wielkości liter,
#   dzięki __icontains)
# - do połączenia warunku "tytuł LUB treść" używamy obiektu Q
#   z django.db.models - pozwala on budować zapytania OR,
#   czego nie da się zrobić samym filter(pole=..., pole2=...),
#   bo to domyślnie działa jak AND
# - jeśli fraza nie została podana, wyświetlamy (tak jak
#   w Zadaniu 3) 5 najnowszych postów
# ------------------------------------------------------------
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Category, Post

LATEST_POSTS_COUNT = 5


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


def home_view(request):
    """
    Widok strony głównej.

    Obsługuje dwa przypadki:
    1. Brak frazy szukanej w GET -> wyświetla 5 najnowszych postów
       (dokładnie jak w Zadaniu 3).
    2. Fraza szukana podana w GET (parametr "q") -> wyświetla
       WSZYSTKIE posty, których tytuł LUB treść zawiera tę frazę
       (bez względu na wielkość liter).
    """
    # Pobieramy frazę z parametru GET o nazwie "q".
    # Jeśli parametru nie ma w URL-u, query przyjmie pusty string.
    query = request.GET.get("q", "").strip()

    if query:
        # Q(...) | Q(...) tworzy warunek OR:
        # tytuł zawiera frazę LUB treść zawiera frazę.
        # icontains = "contains" bez rozróżniania wielkości liter.
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
    else:
        posts = Post.objects.order_by("-publication_date")[:LATEST_POSTS_COUNT]

    context = {
        "posts": posts,
        "query": query,
    }
    return render(request, "blog/home.html", context) 