class Film:
    def __init__(self, tytul, rezyser, rok_produkcji):
        self.tytul = tytul
        self.rezyser = rezyser
        self.rok_produkcji = rok_produkcji

    def informacje(self):
        return f'"{self.tytul}" ({self.rok_produkcji}), reżyseria: {self.rezyser}'


film1 = Film("Incepcja", "Christopher Nolan", 2010)
film2 = Film("Interstellar", "Christopher Nolan", 2014)

print(film1.informacje())
print(film2.informacje())