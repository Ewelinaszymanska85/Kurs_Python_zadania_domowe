lista1 = [1, 1]
lista2 = [1, 1]

print("lista1 is lista2:", lista1 is lista2)
print("lista1 == lista2:", lista1 == lista2)



# Wyjaśnienie:
# "==" sprawdza, czy wartości w listach są takie same → tutaj TAK, więc wynik True.
# "is" sprawdza, czy to ten sam obiekt w pamięci → NIE, bo to dwie osobne listy,
# więc wynik False.