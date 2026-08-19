while True:
    try:
        a = float(input("Podaj pierwszą liczbę: "))
        op = input("Podaj operację (+, -, *, /): ")
        b = float(input("Podaj drugą liczbę: "))

        if op == "+":
            wynik = a + b
        elif op == "-":
            wynik = a - b
        elif op == "*":
            wynik = a * b
        elif op == "/":
            wynik = a / b
        else:
            print("Nieznana operacja.")
            continue

    except ValueError:
        print("Błąd: wpisz poprawne liczby.")
    except ZeroDivisionError:
        print("Błąd: dzielenie przez zero!")
    else:
        print("Wynik:", wynik)
    finally:
        print("Koniec obliczeń.\n") 