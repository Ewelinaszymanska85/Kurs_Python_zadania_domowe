from dataclasses import dataclass

@dataclass
class Film:
    tytul: str
    rezyser: str
    rok_produkcji: int


film1 = Film("Ida", "Paweł Pawlikowski", 2013)
film2 = Film("Zimna wojna", "Paweł Pawlikowski", 2018)

print(film1)
print(film2)