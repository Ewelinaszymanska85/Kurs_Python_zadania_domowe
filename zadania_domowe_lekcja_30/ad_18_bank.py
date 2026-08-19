"""
Symulacja wyścigu w banku.
Pięć wątków wykonuje wpłaty, a pięć wypłaty.
Dostęp do salda jest zabezpieczony przez threading.Lock.
"""
import threading
import random
import time


class KontoBankowe:

    def __init__(self, saldo=0):
        self.saldo = saldo
        self.blokada = threading.Lock()

    def wplac(self, kwota):
        """Wpłaca podaną kwotę na konto."""

        with self.blokada:
            self.saldo += kwota
            print(f"Wpłata +{kwota} zł | Saldo: {self.saldo} zł")

    def wyplac(self, kwota):
        """Wypłaca kwotę, jeśli są dostępne środki."""

        with self.blokada:
            if self.saldo >= kwota:
                self.saldo -= kwota
                print(
                    f"Wypłata -{kwota} zł | "
                    f"Saldo: {self.saldo} zł"
                )
            else:
                print(f"Brak środków na {kwota} zł")


def wplacanie(konto):
    """Wykonuje serię wpłat."""

    for _ in range(10):
        konto.wplac(random.randint(10, 100))
        time.sleep(0.01)


def wyplacanie(konto):
    """Wykonuje serię wypłat."""

    for _ in range(10):
        konto.wyplac(random.randint(10, 100))
        time.sleep(0.01)


if __name__ == "__main__":
    konto = KontoBankowe(1000)
    watki = []

    for _ in range(5):
        watki.append(
            threading.Thread(
                target=wplacanie,
                args=(konto,)
            )
        )

    for _ in range(5):
        watki.append(
            threading.Thread(
                target=wyplacanie,
                args=(konto,)
            )
        )

    for watek in watki:
        watek.start()

    for watek in watki:
        watek.join()

    print(f"\nKońcowe saldo: {konto.saldo} zł")