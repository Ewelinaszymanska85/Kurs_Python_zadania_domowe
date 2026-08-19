class Uzytkownik:
    def __init__(self, wiek):
        self._wiek = wiek

    @property
    def wiek(self):
        return self._wiek

    @wiek.setter
    def wiek(self, nowy_wiek):
        if 0 <= nowy_wiek <= 120:
            self._wiek = nowy_wiek
        else:
            print("Błąd: wiek musi być w zakresie 0–120. Wartość nie została zmieniona.")


# Testowanie
u = Uzytkownik(41)

print(u.wiek)   # getter

u.wiek = 30     # poprawna zmiana
print(u.wiek)

u.wiek = -5     # błąd
print(u.wiek)

u.wiek = 200    # błąd
print(u.wiek) 