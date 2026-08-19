"""
Zadanie domowe 1 - Uwierzytelnianie i Autoryzacja
Konfiguracja settings.py - przekierowania logowania/wylogowania.

Ten fragment pokazuje zmienne dodane do settings.py, które określają
gdzie przekierować użytkownika po zalogowaniu i wylogowaniu.
"""

# Nazwa URL strony logowania - używana m.in. przez dekorator @login_required
LOGIN_URL = 'login'

# Gdzie przekierować użytkownika po udanym zalogowaniu
LOGIN_REDIRECT_URL = 'profile'

# Gdzie przekierować użytkownika po wylogowaniu
LOGOUT_REDIRECT_URL = 'login'