"""
Zadanie domowe 8 - Uwierzytelnianie i Autoryzacja
Zmiana hasła - PasswordChangeView i PasswordChangeDoneView.

Kompletne rozwiązanie zadania wykorzystuje w całości wbudowane
widoki Django - nie wymaga pisania własnej logiki, tylko podpięcia
odpowiednich ścieżek URL i stworzenia dwóch prostych szablonów.

============================================================
1. ŚCIEŻKI URL (proj/urls.py) - fragment do dodania:
============================================================

from django.contrib.auth import views as auth_views

urlpatterns = [
    # ... istniejące ścieżki

    path(
        'password_change/',
        auth_views.PasswordChangeView.as_view(
            template_name='users/password_change_form.html'
        ),
        name='password_change'
    ),
    path(
        'password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html'
        ),
        name='password_change_done'
    ),
]

============================================================
2. SZABLON (templates/users/password_change_form.html):
============================================================

{% extends "base.html" %}
{% block title %}Zmiana hasła{% endblock %}
{% block content %}
    <div class="content-section">
        <form method="POST">
            {% csrf_token %}
            <fieldset class="form-group">
                <legend class="border-bottom mb-4">Zmień hasło</legend>
                {{ form.as_p }}
            </fieldset>
            <div class="form-group">
                <button type="submit">Zmień hasło</button>
            </div>
        </form>
    </div>
{% endblock content %}

============================================================
3. SZABLON (templates/users/password_change_done.html):
============================================================

{% extends "base.html" %}
{% block title %}Hasło zmienione{% endblock %}
{% block content %}
    <div class="content-section">
        <h2>Hasło zostało pomyślnie zmienione!</h2>
        <p><a href="{% url 'profile' %}">Wróć do profilu</a></p>
    </div>
{% endblock content %}
"""