class Pracownik:
    def __init__(self, imie, stawka_godzinowa):
        self.imie = imie
        self.stawka_godzinowa = stawka_godzinowa

    def oblicz_pensje(self, liczba_godzin):
        return self.stawka_godzinowa * liczba_godzin


class Programista(Pracownik):
    def __init__(self, imie, stawka_godzinowa, jezyki_programowania):
        super().__init__(imie, stawka_godzinowa)
        self.jezyki_programowania = jezyki_programowania


programista1 = Programista("Ewelina", 95, ["Python", "JavaScript", "C++"])

pensja = programista1.oblicz_pensje(160)
print(f"{programista1.imie} zarobi: {pensja} zł") 