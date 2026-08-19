def kalkulator(a, b, operacja):
    # Wykonanie odpowiedniej operacji w zależności od znaku
    if operacja == "+":
        return a + b
    elif operacja == "-":
        return a - b
    elif operacja == "*":
        return a * b
    elif operacja == "/":
        # Zabezpieczenie przed dzieleniem przez zero
        if b == 0:
            return "Błąd: dzielenie przez zero"
        return a / b
    else:
        return "Nieznana operacja"


print(kalkulator(10, 5, "+"))
print(kalkulator(10, 5, "-"))
print(kalkulator(10, 5, "*"))
print(kalkulator(10, 5, "/")) 