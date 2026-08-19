"""
Zadanie domowe 7 - Middleware, JWT i Uwierzytelnianie w DRF
Tworzenie własnego Middleware - logowanie metody HTTP.

Kompletne rozwiązanie zadania obejmuje dwa elementy:
1. Klasa middleware (poniżej, aktywny kod)
2. Rejestracja w settings.py (dołączona jako komentarz referencyjny)

============================================================
1. MIDDLEWARE (authproject/middleware.py)
============================================================
"""


class SimpleLoggingMiddleware:
    """
    Middleware logujący do konsoli metodę HTTP każdego
    przychodzącego zapytania.
    """

    def __init__(self, get_response):
        """
        Jednorazowa konfiguracja i inicjalizacja middleware,
        wykonywana raz przy starcie serwera.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Wykonywane dla każdego zapytania.
        """
        print(f"Otrzymano zapytanie metodą {request.method} na ścieżkę: {request.path}")

        response = self.get_response(request)

        print(f"Zwracam odpowiedź z kodem statusu: {response.status_code}")

        return response


"""
============================================================
2. REJESTRACJA (authproject/settings.py) - fragment MIDDLEWARE:
============================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'authproject.middleware.SimpleLoggingMiddleware',
]

============================================================
3. WYNIK TESTU (fragment logów terminala)
============================================================

Otrzymano zapytanie metodą GET na ścieżkę: /admin/
Zwracam odpowiedź z kodem statusu: 200
[08/Jul/2026 11:37:34] "GET /admin/ HTTP/1.1" 200 6023
"""