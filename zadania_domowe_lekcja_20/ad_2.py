# =============================================================================
# ZADANIE 2: Stwórz dynamiczną trasę
# =============================================================================


# -----------------------------------------------------------------------------
# pages/views.py
# -----------------------------------------------------------------------------
from django.http import HttpResponse


def info_view(request):
    """Widok funkcyjny dla trasy /info/ - zwraca prosty tekst."""
    return HttpResponse("Informacje o stronie")


def rules_view(request):
    """Widok funkcyjny dla trasy /rules/ - zwraca prosty tekst."""
    return HttpResponse("Regulamin")


def user_profile_view(request, username):
    """Widok funkcyjny dla trasy /user/<username>/."""
    return HttpResponse(f"Witaj na profilu, {username}!")


# -----------------------------------------------------------------------------
# pages/urls.py
# -----------------------------------------------------------------------------
from django.urls import path
from . import views

urlpatterns = [
    path('info/', views.info_view, name='info'),
    path('rules/', views.rules_view, name='rules'),
    path('user/<str:username>/', views.user_profile_view, name='user-profile'),
] 