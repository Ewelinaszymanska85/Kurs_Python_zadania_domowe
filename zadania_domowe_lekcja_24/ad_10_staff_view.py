"""
Zadanie domowe 10 - Uwierzytelnianie i Autoryzacja
Widok tylko dla admina - @staff_member_required.

Kompletne rozwiązanie zadania obejmuje trzy elementy:
1. Widok (poniżej, aktywny kod)
2. Ścieżkę URL w users/urls.py (dołączona jako komentarz referencyjny)
3. Szablon user_list.html (dołączony jako komentarz referencyjny)

============================================================
1. WIDOK (proj/users/views.py)
============================================================
"""

from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User


@staff_member_required
def user_list(request):
    """
    Widok wyświetlający listę wszystkich zarejestrowanych użytkowników.

    Dostępny wyłącznie dla użytkowników ze statusem is_staff=True
    (czyli personelu/administratorów), dzięki dekoratorowi
    @staff_member_required. Zwykli użytkownicy próbujący wejść
    na tę stronę zostaną przekierowani na stronę logowania
    administracyjnego.
    """
    users = User.objects.all()
    return render(request, 'users/user_list.html', {'users': users})


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
    path('users/', views.user_list, name='user_list'),
]

============================================================
3. SZABLON (templates/users/user_list.html) - pełna zawartość:
============================================================

{% extends "base.html" %}
{% block title %}Lista użytkowników{% endblock %}
{% block content %}
    <div class="content-section">
        <h1>Lista zarejestrowanych użytkowników</h1>
        <table style="width: 100%; border-collapse: collapse;">
            <thead>
                <tr style="border-bottom: 2px solid #333;">
                    <th style="text-align: left; padding: 8px;">Nazwa użytkownika</th>
                    <th style="text-align: left; padding: 8px;">Email</th>
                    <th style="text-align: left; padding: 8px;">Personel (staff)</th>
                    <th style="text-align: left; padding: 8px;">Data dołączenia</th>
                </tr>
            </thead>
            <tbody>
                {% for u in users %}
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 8px;">{{ u.username }}</td>
                    <td style="padding: 8px;">{{ u.email|default:"—" }}</td>
                    <td style="padding: 8px;">{{ u.is_staff|yesno:"Tak,Nie" }}</td>
                    <td style="padding: 8px;">{{ u.date_joined|date:"d.m.Y" }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
{% endblock content %}
""" 