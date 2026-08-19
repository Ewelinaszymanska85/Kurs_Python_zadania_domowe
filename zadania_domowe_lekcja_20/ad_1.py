# =============================================================================
# ZADANIE 1: Stwórz statyczne trasy i widoki
# =============================================================================
# Zadanie wymaga zmian w 4 plikach. Każdy fragment poniżej pokazuje finalną
# wersję odpowiedniego pliku/sekcji, ze ścieżką względną w komentarzu.


# -----------------------------------------------------------------------------
# le20/settings.py  (fragment - sekcja INSTALLED_APPS)
# -----------------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pages',
]


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


# -----------------------------------------------------------------------------
# pages/urls.py  (nowy plik - trzeba go utworzyć w folderze pages/)
# -----------------------------------------------------------------------------
from django.urls import path
from . import views

urlpatterns = [
    path('info/', views.info_view, name='info'),
    path('rules/', views.rules_view, name='rules'),
]


# -----------------------------------------------------------------------------
# le20/urls.py  (główny plik URL projektu - dodajemy include do pages.urls)
# -----------------------------------------------------------------------------
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
] 