def kalkulator(a: float, b: float, operacja: str) -> float | str:
    """
    Wykonuje podstawowe działania matematyczne na dwóch liczbach.

    Funkcja przyjmuje dwie liczby oraz znak operacji i zwraca wynik działania.
    Obsługiwane operacje to: dodawanie, odejmowanie, mnożenie i dzielenie.

    Parametry:
    a (float): pierwsza liczba
    b (float): druga liczba
    operacja (str): znak operacji matematycznej ("+", "-", "*", "/")

    Zwraca:
    float | str: wynik działania lub komunikat o błędzie (np. przy dzieleniu przez 0 lub złej operacji)
    """

    if operacja == "+":
        return a + b
    elif operacja == "-":
        return a - b
    elif operacja == "*":
        return a * b
    elif operacja == "/":
        if b == 0:
            return "Błąd: dzielenie przez zero"
        return a / b
    else:
        return "Nieznana operacja"