"""
Zadanie domowe 8 - Middleware, JWT i Uwierzytelnianie w DRF
Chroniony endpoint - APIView z IsAuthenticated.

Kompletne rozwiązanie zadania obejmuje trzy elementy:
1. Widok ProtectedView (poniżej, aktywny kod)
2. Ścieżkę URL w api/urls.py (dołączona jako komentarz referencyjny)
3. Podłączenie w głównym urls.py (dołączone jako komentarz referencyjny)

============================================================
1. WIDOK (api/views.py)
============================================================
"""

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class ProtectedView(APIView):
    """
    Prosty, chroniony endpoint dostępny tylko dla zalogowanych
    użytkowników (uwierzytelnionych poprawnym tokenem JWT).
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Zwraca nazwę zalogowanego użytkownika.

        Dzięki JWTAuthentication (skonfigurowanemu globalnie
        w REST_FRAMEWORK) oraz permission_classes = [IsAuthenticated],
        DRF automatycznie odrzuci zapytanie z kodem 401, jeśli
        nagłówek Authorization z poprawnym tokenem nie zostanie
        dołączony.
        """
        return Response({"message": f"Witaj, {request.user.username}!"})


"""
============================================================
2. ŚCIEŻKA URL (api/urls.py) - pełna zawartość:
============================================================

from django.urls import path
from .views import ProtectedView

urlpatterns = [
    path('protected/', ProtectedView.as_view(), name='protected'),
]

============================================================
3. PODŁĄCZENIE (authproject/urls.py) - fragment do dodania:
============================================================

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/', include('api.urls')),
]

============================================================
4. WYNIKI TESTÓW W POSTMANIE
============================================================

Test 1: GET /api/protected/ - bez tokenu
Response: 401 Unauthorized
{"detail": "Authentication credentials were not provided."}

Test 2: GET /api/protected/ - z poprawnym tokenem (Authorization: Bearer <token>)
Response: 200 OK
{"message": "Witaj, testowy_user!"}
""" 