# Zadanie 3 – Wyświetlanie ID

# W wersji Raw SQL wyświetlamy ID przez indeks:
# print(f"ID: {z[0]} | {z[1]} | {status}")
# z[0] = id, z[1] = tytul, z[2] = ukonczone

# W wersji ORM wyświetlamy ID przez atrybut obiektu:
# print(f"ID: {z.id} | {z.tytul} | {status}")
# Działa bo Zadanie to klasa z atrybutami id, tytul, ukonczone

# Różnica: ORM jest czytelniejszy - używamy nazw zamiast indeksów