class Figura:
    def oblicz_pole(self):
        pass


class Kwadrat(Figura):
    def __init__(self, bok):
        self.bok = bok

    def oblicz_pole(self):
        return self.bok ** 2


class Kolo(Figura):
    def __init__(self, promien):
        self.promien = promien

    def oblicz_pole(self):
        PI = 3.14159
        return PI * (self.promien ** 2) 


figury = [
    Kwadrat(4),
    Kolo(3)
]

for figura in figury:
    print(figura.oblicz_pole())