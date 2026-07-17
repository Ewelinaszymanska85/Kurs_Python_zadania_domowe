"""
Zadanie domowe 9 - Uwierzytelnianie i Autoryzacja
Automatyczne logowanie po rejestracji.

Zaktualizowany widok register, który po pomyślnym
utworzeniu konta automatycznie loguje nowego użytkownika, korzystając
z funkcji login() z django.contrib.auth, zamiast przekierowywać
go na osobną stronę logowania.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from proj.users.forms import CustomUserCreationForm


def register(request):
    """
    Widok obsługujący rejestrację nowego użytkownika.

    Po pomyślnej walidacji formularza:
    1. Zapisuje nowego użytkownika w bazie danych (form.save()).
    2. Automatycznie go loguje za pomocą funkcji login(request, user),
       tworząc dla niego aktywną sesję - bez potrzeby ręcznego
       logowania się po rejestracji.
    3. Przekierowuje na stronę główną (zamiast na stronę logowania).
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Witaj, {user.username}! Twoje konto zostało utworzone i zostałeś zalogowany.')
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form}) 