"""
Zadanie domowe 3 - Uwierzytelnianie i Autoryzacja
Strona profilu - widok chroniony @login_required.

Prosty widok wyświetlający powitanie zalogowanego
użytkownika, dostępny wyłącznie dla osób zalogowanych.
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def profile(request):
    """
    Widok strony profilu użytkownika.

    Dekorator @login_required sprawdza, czy użytkownik jest zalogowany.
    Jeśli nie, automatycznie przekierowuje go na stronę logowania
    zdefiniowaną w LOGIN_URL, dołączając parametr ?next=/profile/,
    żeby po zalogowaniu wrócić dokładnie tutaj.
    """
    return render(request, 'users/profile.html')