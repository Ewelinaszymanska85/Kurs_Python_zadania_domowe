# Próba błędnej konwersji (spowoduje ValueError)
# liczba = int("Python")

# Wyjaśnienie:
# Nie da się zamienić tekstu "Python" na liczbę całkowitą,
# ponieważ nie jest to zapis liczbowy.
# Funkcja int() działa tylko dla ciągów zawierających cyfry, np. "123".


# Poprawny przykład:
liczba = int("123")
print(liczba) 