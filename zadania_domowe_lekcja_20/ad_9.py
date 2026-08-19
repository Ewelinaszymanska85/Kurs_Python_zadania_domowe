# ============================================================
# Zadanie 9 - Filtrowanie po kategorii
# ============================================================


# ------------------------------------------------------------
# le20/pages/views.py
# (dopisać na końcu pliku istniejących widoków - reszta bez zmian)
# ------------------------------------------------------------
def category_products_view(request, category_id):
    """Widok wyświetlający produkty należące do danej kategorii."""
    products = Product.objects.filter(category_id=category_id)
    return render(request, "pages/product_list.html", {"products": products})


# ------------------------------------------------------------
# le20/pages/urls.py
# (dopisać nową ścieżkę do listy urlpatterns - reszta bez zmian)
# ------------------------------------------------------------
from django.urls import path
from . import views

urlpatterns = [
    path('info/', views.info_view, name='info'),
    path('rules/', views.rules_view, name='rules'),
    path('user/<str:username>/', views.user_profile_view, name='user-profile'),
    path('products/', views.product_list_view, name='product-list'),
    path('notes/', views.note_list_view, name='note-list'),
    path('note/<int:note_id>/', views.note_detail_view, name='note-detail'),
    path('add_product/', views.add_product, name='add_product'),
    path('category/<int:category_id>/', views.category_products_view, name='category-products'),
] 