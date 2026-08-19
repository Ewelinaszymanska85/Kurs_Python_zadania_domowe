def stworz_profil(imie, **dane_dodatkowe):
    """
    Tworzy profil użytkownika w postaci słownika.

    Parametry:
    imie (str): imię użytkownika (wymagane)
    **dane_dodatkowe: dowolne dodatkowe informacje (np. wiek, miasto)

    Zwraca:
    dict: słownik zawierający dane profilu
    """

    # Tworzymy słownik z obowiązkowym imieniem
    profil = {"imie": imie}

    # Dodajemy wszystkie dodatkowe dane do słownika
    profil.update(dane_dodatkowe)

    return profil


print(stworz_profil("EWELINA", wiek=41, miasto="STARGARD"))
print(stworz_profil("Jan", zawod="programista", hobby="piłka nożna")) 