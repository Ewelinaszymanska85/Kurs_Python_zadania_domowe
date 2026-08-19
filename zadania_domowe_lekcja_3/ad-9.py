a = int(input("Podaj pierwszą wartość (1 = True, 0 = False): "))
b = int(input("Podaj drugą wartość (1 = True, 0 = False): "))

a = bool(a)
b = bool(b)

print("AND:", a and b)
print("OR:", a or b) 