class Punkt:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"


punkt1 = Punkt(3, 5)
punkt2 = Punkt(-1, 7)

print(punkt1)
print(punkt2) 