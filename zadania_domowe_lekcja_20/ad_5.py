# =============================================================================
# ZADANIE 5: Stwórz szablon bazowy
# =============================================================================


# -----------------------------------------------------------------------------
# templates/base.html
# -----------------------------------------------------------------------------
base_html = """
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Moja Strona{% endblock %}</title>
</head>
<body>
    <header>
        <h1>Witaj na mojej stronie!</h1>
    </header>
    <main>
        {% block content %}
        {% endblock %}
    </main>
</body>
</html>
"""


# -----------------------------------------------------------------------------
# pages/templates/pages/product_list.html
# (zaktualizowany, żeby dziedziczył po base.html)
# -----------------------------------------------------------------------------
product_list_html = """
{% extends "base.html" %}

{% block title %}Lista produktów{% endblock %}

{% block content %}
<h2>Produkty</h2>
<ul>
    {% for product in products %}
    <li>{{ product.name }} - {{ product.price }} zł</li>
    {% endfor %}
</ul>
{% endblock %}
""" 