from dataclasses import dataclass

class BrakSrodkowError(Exception):
    pass


@dataclass
class KontoBankowe:
    _saldo: float = 0.0

    @property
    def saldo(self):
        return self._saldo

    def wplac(self, kwota):
        if kwota < 0:
            raise ValueError("Kwota wpłaty nie może być ujemna.")
        self._saldo += kwota

    def wyplac(self, kwota):
        if kwota < 0:
            raise ValueError("Kwota wypłaty nie może być ujemna.")
        if kwota > self._saldo:
            raise BrakSrodkowError("Brak wystarczających środków na koncie.")
        self._saldo -= kwota


# Testowanie
konto = KontoBankowe()

operacje = [
    ("wplata", 100),
    ("wyplata", 50),
    ("wyplata", 100),   # brak środków
    ("wplata", -20),    # błąd
]

for operacja, kwota in operacje:
    try:
        if operacja == "wplata":
            konto.wplac(kwota)
            print(f"Wpłacono {kwota}. Saldo: {konto.saldo}")
        elif operacja == "wyplata":
            konto.wyplac(kwota)
            print(f"Wypłacono {kwota}. Saldo: {konto.saldo}")

    except ValueError as e:
        print(f"BŁĄD: {e}")
    except BrakSrodkowError as e:
        print(f"BŁĄD: {e}") 