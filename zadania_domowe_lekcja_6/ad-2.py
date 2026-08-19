def opis_ksiazki(tytul, autor, rok_wydania=2024):
# Zwraca sformatowany opis książki
    return f"Książka '{tytul}' została napisana przez {autor} i wydana w roku {rok_wydania}."


# Wywołanie z argumentami pozycyjnymi
print(opis_ksiazki("Pan Tadeusz", "Adam Mickiewicz", 1834))

# Wywołanie z argumentami nazwanymi
print(opis_ksiazki(autor="Henryk Sienkiewicz", tytul="Quo Vadis", rok_wydania=1896))

# Wywołanie z domyślnym rokiem wydania
print(opis_ksiazki("Przykładowa książka", "Karol Kowalski")) 