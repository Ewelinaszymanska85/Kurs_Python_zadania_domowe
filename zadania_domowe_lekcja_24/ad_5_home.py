"""
Zadanie domowe 5 - Uwierzytelnianie i Autoryzacja
Strona główna zabezpieczona @login_required.

Kompletne rozwiązanie zadania obejmuje trzy elementy:
1. Widok (poniżej, aktywny kod)
2. Ścieżkę URL w users/urls.py (dołączona jako komentarz referencyjny)
3. Szablon home.html (dołączony jako komentarz referencyjny)

============================================================
1. WIDOK (proj/users/views.py)
============================================================
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    """
    Widok strony głównej aplikacji.

    Dekorator @login_required sprawdza, czy użytkownik jest zalogowany.
    Niezalogowani użytkownicy zostaną automatycznie przekierowani na
    stronę logowania (zgodnie z LOGIN_URL w settings.py), z parametrem
    ?next=/, żeby po zalogowaniu wrócić właśnie tutaj.
    """
    return render(request, 'users/home.html')


"""
============================================================
2. ŚCIEŻKA URL (proj/users/urls.py) - fragment do dodania:
============================================================

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]

============================================================
3. SZABLON (templates/users/home.html) - pełna zawartość:
============================================================

{% extends "base.html" %}
{% block title %}Strona główna{% endblock %}
{% block content %}
    <div class="content-section">
        <h1>Strona główna</h1>
        <p>Witaj, {{ user.username }}! To jest chroniona strona główna aplikacji.</p>
    </div>
{% endblock content %}

============================================================
4. USTAWIENIA (proj/settings.py) - wymagana zmiana:
============================================================

LOGIN_REDIRECT_URL = 'home'
""" 