"""
Zadanie domowe 7 - Wprowadzenie do Django REST Framework
API Kalkulatora - widok funkcyjny z obsługą błędów.

Kompletne rozwiązanie zadania obejmuje dwa elementy:
1. Widok funkcyjny calculate_view (poniżej, aktywny kod)
2. Ścieżkę URL w głównym urls.py (dołączona jako komentarz
   referencyjny)

============================================================
1. WIDOK (tasks/views.py)
============================================================
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def calculate_view(request):
    """
    Widok wykonujący podstawowe operacje matematyczne na podstawie
    parametrów zapytania.

    Oczekiwane parametry zapytania:
        num1 (float): Pierwsza liczba.
        num2 (float): Druga liczba.
        operation (str): Jedna z wartości 'add', 'subtract',
                          'multiply', 'divide'.

    Przykładowe użycie:
        /api/calculate/?num1=10&num2=5&operation=add

    Zwraca:
        JSON z wynikiem operacji, np. {"result": 15}, lub błąd
        z odpowiednim kodem HTTP w przypadku niepoprawnych danych.
    """
    num1_raw = request.query_params.get('num1')
    num2_raw = request.query_params.get('num2')
    operation = request.query_params.get('operation')

    if num1_raw is None or num2_raw is None or operation is None:
        return Response(
            {"error": "Wymagane parametry: num1, num2, operation."},
            status=400
        )

    try:
        num1 = float(num1_raw)
        num2 = float(num2_raw)
    except ValueError:
        return Response(
            {"error": "num1 i num2 muszą być liczbami."},
            status=400
        )

    if operation == 'add':
        result = num1 + num2
    elif operation == 'subtract':
        result = num1 - num2
    elif operation == 'multiply':
        result = num1 * num2
    elif operation == 'divide':
        if num2 == 0:
            return Response(
                {"error": "Nie można dzielić przez zero."},
                status=400
            )
        result = num1 / num2
    else:
        return Response(
            {"error": f"Nieznana operacja: '{operation}'. Dozwolone: add, subtract, multiply, divide."},
            status=400
        )

    return Response({"result": result})


"""
============================================================
2. ŚCIEŻKA URL (taskmanger/urls.py) - fragment do dodania:
============================================================

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/calculate/', views.calculate_view, name='calculate'),
]

============================================================
3. WYNIKI TESTÓW
============================================================

Test 1: /api/calculate/?num1=10&num2=5&operation=add
Wynik: {"result": 15.0} - HTTP 200 OK

Test 2: /api/calculate/?num1=10&num2=0&operation=divide
Wynik: {"error": "Nie można dzielić przez zero."} - HTTP 400 Bad Request

Test 3: /api/calculate/?num1=10&num2=5&operation=power
Wynik: {"error": "Nieznana operacja: 'power'. Dozwolone: add, subtract, multiply, divide."} - HTTP 400 Bad Request
"""