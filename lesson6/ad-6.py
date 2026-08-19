def wielokrotne_powitanie(imie: str, ilosc: int) -> None:
    """
    Wyświetla powitanie podaną liczbę razy.

    Funkcja drukuje komunikat "Cześć, {imie}!" tyle razy,
    ile wynosi parametr ilosc. Nie zwraca żadnej wartości.

    Parametry:
    imie (str): imię osoby do powitania
    ilosc (int): liczba powtórzeń

    Zwraca:
    None
    """

    for _ in range(ilosc):
        print(f"Cześć, {imie}!")


wielokrotne_powitanie("EWELINA", 3) 