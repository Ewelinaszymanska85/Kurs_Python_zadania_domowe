x = 10

print("Wartość x:", x)
print("ID x:", id(x))

x = x + 1

print("Nowa wartość x:", x)
print("Nowe ID x:", id(x))



# Czy identyfikator się zmienił?

# Tak, identyfikator może się zmienić, ponieważ liczby całkowite
# (typ int) są niemutowalne (immutable).
# Instrukcja x = x + 1 tworzy nowy obiekt o wartości 11,
# a zmienna x zaczyna wskazywać na ten nowy obiekt.