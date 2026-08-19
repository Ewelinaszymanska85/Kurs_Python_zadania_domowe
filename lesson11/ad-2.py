class Produkt:
    def __init__(self, nazwa, cena, kategoria):
        self.nazwa = nazwa
        self.cena = cena
        self.kategoria = kategoria


produkt1 = Produkt("Laptop", 1999.99, "Elektronika")

print(produkt1.nazwa)
print(produkt1.cena)
print(produkt1.kategoria) 