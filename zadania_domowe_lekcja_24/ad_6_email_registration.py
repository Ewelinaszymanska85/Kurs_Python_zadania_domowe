"""
Zadanie domowe 6 - Uwierzytelnianie i Autoryzacja
Rozszerzenie formularza rejestracji o pole email.

Kompletne rozwiązanie zadania obejmuje dwa elementy:
1. Własny formularz CustomUserCreationForm (poniżej, aktywny kod)
2. Zaktualizowany widok register, korzystający z tego formularza
   (dołączony jako komentarz referencyjny)

============================================================
1. FORMULARZ (proj/users/forms.py)
============================================================
"""

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class CustomUserCreationForm(UserCreationForm):
    """
    Rozszerzony formularz rejestracji, dodający pole email
    do standardowego UserCreationForm.

    Pole email jest wymagane i zostaje zapisane razem
    z nowo utworzonym użytkownikiem w bazie danych.
    """

    email = forms.EmailField(
        required=True,
        help_text="Podaj prawidłowy adres email."
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def save(self, commit=True):
        """
        Zapisuje użytkownika wraz z adresem email.

        Args:
            commit (bool): Czy od razu zapisać obiekt w bazie danych.

        Returns:
            User: Nowo utworzony obiekt użytkownika.
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


"""
============================================================
2. WIDOK (proj/users/views.py) - zaktualizowana funkcja register:
============================================================

from django.shortcuts import render, redirect
from django.contrib import messages
from proj.users.forms import CustomUserCreationForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Konto dla {username} zostało utworzone! Możesz się teraz zalogować.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})
"""