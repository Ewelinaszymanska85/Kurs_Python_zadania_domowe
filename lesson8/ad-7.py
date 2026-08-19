# Wersja 1 – z metodą .get()
def pobierz_wartosc(slownik, klucz):
    return slownik.get(klucz)

# Wersja 2 – z try...except
def pobierz_wartosc_try(slownik, klucz):
    try:
        return slownik[klucz]
    except KeyError:
        return None

# Testy
dane = {"imie": "Ania", "wiek": 25}

print(pobierz_wartosc(dane, "imie"))   # Ania
print(pobierz_wartosc(dane, "adres"))  # None

print(pobierz_wartosc_try(dane, "imie"))   # Ania
print(pobierz_wartosc_try(dane, "adres"))  # None
