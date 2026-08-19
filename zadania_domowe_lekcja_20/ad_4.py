# =============================================================================
# ZADANIE 4: Wyświetl dane w szablonie
# =============================================================================


# Komendy wykonane w manage.py shell (dodanie danych testowych):
#
#     python manage.py shell
#
#     from pages.models import Product
#     Product.objects.create(name="Laptop", description="Laptop do pracy i nauki", price=2999.99)
#     Product.objects.create(name="Mysz bezprzewodowa", description="Ergonomiczna mysz", price=89.90)
#     Product.objects.create(name="Klawiatura mechaniczna", description="Klawiatura z podświetleniem", price=349.00)
#     exit()


# -----------------------------------------------------------------------------
# pages/views.py  (fragment - dodany widok product_list_view)
# -----------------------------------------------------------------------------
from django.shortcuts import render
from .models import Product


def product_list_view(request):
    """Widok wyświetlający listę produktów z bazy danych."""
    products = Product.objects.all()
    return render(request, "pages/product_list.html", {"products": products})


# -----------------------------------------------------------------------------
# pages/urls.py  (fragment - dodana trasa products/)
# -----------------------------------------------------------------------------
urlpatterns_fragment = """
path('products/', views.product_list_view, name='product-list'),
"""


# -----------------------------------------------------------------------------
# pages/templates/pages/product_list.html
# -----------------------------------------------------------------------------
product_list_html = """
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <title>Lista produktów</title>
</head>
<body>
    <h1>Produkty</h1>
    <ul>
        {% for product in products %}
        <li>{{ product.name }} - {{ product.price }} zł</li>
        {% endfor %}
    </ul>
</body>
</html>
""" 