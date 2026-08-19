class WiekNiepoprawnyError(Exception):
    pass

def rejestruj_uzytkownika(wiek):
    if wiek < 18:
        raise WiekNiepoprawnyError("Użytkownik musi mieć co najmniej 18 lat.")
    return "Rejestracja zakończona sukcesem!"

try:
    wiek = int(input("Podaj swój wiek: "))
    komunikat = rejestruj_uzytkownika(wiek)
except ValueError:
    print("Błąd: podaj poprawną liczbę.")
except WiekNiepoprawnyError as e:
    print("Błąd:", e)
else:
    print(komunikat)
finally:
    print("Koniec procesu rejestracji.")