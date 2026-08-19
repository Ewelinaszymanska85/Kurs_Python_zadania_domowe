while True:
    try:
        a = float(input("Podaj pierwszą liczbę: "))
        b = float(input("Podaj drugą liczbę: "))
        operacja = input("Podaj operację (+, -, *, /): ")

        if operacja == "+":
            wynik = a + b
        elif operacja == "-":
            wynik = a - b
        elif operacja == "*":
            wynik = a * b
        elif operacja == "/":
            if b == 0:
                raise ZeroDivisionError
            wynik = a / b
        else:
            print("Nieznana operacja")
            continue

    except ValueError:
        print("Błąd wartości: wpisz poprawne liczby")
    except ZeroDivisionError:
        print("Błąd: nie można dzielić przez zero.")
    else:
        print("Wynik:", wynik)
    finally:
        print("Kolejna operacja...\n")
        