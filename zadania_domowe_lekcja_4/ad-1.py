a = float(input("Podaj pierwszą liczbę: "))
b = float(input("Podaj drugą liczbę: "))

print("Dodawanie:", a + b)
print("Odejmowanie:", a - b)
print("Mnożenie:", a * b)

# zabezpieczenie przed dzieleniem przez 0
if b != 0:
    print("Dzielenie:", a / b)
else:
    print("Nie można dzielić przez zero!") 