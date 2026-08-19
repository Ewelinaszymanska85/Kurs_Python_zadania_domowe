# ============================================================
# Lekcja 22 - Zadanie 3 - Ostatnie Posty na Stronie Głównej
# ============================================================


# ------------------------------------------------------------
# blog/views.py
# (dopisz tę funkcję na końcu pliku, pod category_posts_view)
# ------------------------------------------------------------
def home_view(request):
    """
    Widok strony głównej wyświetlający 5 najnowszych postów.
    """
    posts = Post.objects.order_by('-publication_date')[:5]
    context = {"posts": posts}
    return render(request, "blog/home.html", context)


# ------------------------------------------------------------
# blog/urls.py
# (CAŁY PLIK - zastąp obecną zawartość tą wersją; dodany import
#  home_view oraz nowa ścieżka do strony głównej)
# ------------------------------------------------------------
from django.urls import path
from .views import category_posts_view, home_view

urlpatterns = [
    path("", home_view, name="home"),
    path("category/<int:category_id>/", category_posts_view, name="category-posts"),
] 