class Instrument:
    def graj(self):
        return "Wydaje dźwięk."


class Strunowy(Instrument):
    def graj(self):
        return super().graj() + " [Szarpnięcie struny]"


class Dety(Instrument):
    def graj(self):
        return super().graj() + " [Dmuchnięcie w ustnik]"


class Gitara(Strunowy):
    def graj(self):
        return super().graj() + " [Akord G-dur]"


class Trabka(Dety):
    def graj(self):
        return super().graj() + " [Fanfara]"


# Testowanie
instrument = Instrument()
strunowy = Strunowy()
gitara = Gitara()
trabka = Trabka()

print(instrument.graj())
print(strunowy.graj())
print(gitara.graj())
print(trabka.graj())