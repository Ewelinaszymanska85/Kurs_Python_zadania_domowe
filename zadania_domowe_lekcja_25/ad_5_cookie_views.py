"""
Zadanie domowe 5 - Wprowadzenie do Django REST Framework
Widok z ciasteczkiem - set-name i hello.

Kompletne rozwiązanie zadania obejmuje dwa elementy:
1. Widoki funkcyjne (poniżej, aktywny kod)
2. Ścieżki URL w głównym urls.py (dołączone jako komentarz
   referencyjny)

============================================================
1. WIDOKI (tasks/views.py) - fragment z nowymi funkcjami
============================================================
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def set_name_view(request):
    """
    Widok ustawiający ciasteczko 'user_name' na podstawie
    parametru zapytania 'name'.

    Przykładowe użycie: /api/set-name/?name=Anna

    Jeśli parametr 'name' nie zostanie podany, używana jest
    domyślna wartość 'Gość'.
    """
    name = request.query_params.get('name', 'Gość')
    response = Response({"message": f"Ciasteczko ustawione na: {name}"})
    response.set_cookie('user_name', name, max_age=3600)
    return response


@api_view(['GET'])
def hello_view(request):
    """
    Widok odczytujący ciasteczko 'user_name' i zwracający
    spersonalizowane powitanie.

    Jeśli ciasteczko nie istnieje (np. set_name_view nie było
    jeszcze wywołane), zwraca powitanie dla "Gościa".
    """
    name = request.COOKIES.get('user_name', 'Gość')
    return Response({"message": f"Witaj, {name}!"})


"""
============================================================
2. ŚCIEŻKI URL (taskmanger/urls.py) - fragment do dodania:
============================================================

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/set-name/', views.set_name_view, name='set_name'),
    path('api/hello/', views.hello_view, name='hello'),
]
""" 