# Wartość 256
a = 256
b = 256
c = 256

print("ID dla 256:")
print(id(a))
print(id(b))
print(id(c))

# Wartość 257
x = 257
y = 257
z = 257

print("\nID dla 257:")
print(id(x))
print(id(y))
print(id(z)) 

# Wyjaśnienie:
# Python "cache'uje" (internuje) małe liczby całkowite z zakresu -5 do 256.
# Dlatego zmienne a, b, c wskazują na ten sam obiekt w pamięci (to samo id).
# Dla 257 Python tworzy nowe obiekty, więc id(x), id(y), id(z) są różne.