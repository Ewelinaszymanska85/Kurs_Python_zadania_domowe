class Wektor2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Dodawanie wektorów
    def __add__(self, other):
        return Wektor2D(self.x + other.x, self.y + other.y)

    # Odejmowanie wektorów
    def __sub__(self, other):
        return Wektor2D(self.x - other.x, self.y - other.y)

    # Porównywanie wektorów
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    # Ładne wyświetlanie
    def __str__(self):
        return f"({self.x}, {self.y})"


# Tworzenie wektorów
wektor1 = Wektor2D(3, 5)
wektor2 = Wektor2D(1, 2)

# Dodawanie
suma = wektor1 + wektor2

# Odejmowanie
roznica = wektor1 - wektor2

# Porównywanie
czy_rowne = wektor1 == wektor2

# Wyświetlanie wyników
print("Wektor 1:", wektor1)
print("Wektor 2:", wektor2)
print("Suma:", suma)
print("Różnica:", roznica)
print("Czy są równe?", czy_rowne)