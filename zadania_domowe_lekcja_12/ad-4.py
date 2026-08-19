def bezpieczne_dzielenie(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        print("Błąd: Dzielenie przez zero!")
        return None


print(bezpieczne_dzielenie(10, 2))   # 5.0
print(bezpieczne_dzielenie(10, 0))   # None + komunikat