def oblicz_srednia(lista_ocen):
    assert len(lista_ocen) > 0, "Lista ocen nie może być pusta!"
    return sum(lista_ocen) / len(lista_ocen)

try:
    oceny = [4, 5, 3, 4, 5]
    print(f"Średnia: {oblicz_srednia(oceny):.2f}")

    pusta = []
    print(f"Średnia: {oblicz_srednia(pusta):.2f}")

except AssertionError as e:
    print(f"Błąd: {e}") 
    