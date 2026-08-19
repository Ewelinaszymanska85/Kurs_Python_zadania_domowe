log_file = open("log.txt", "a", encoding="utf-8")

try:
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
                    raise ZeroDivisionError("Nie można dzielić przez zero!")
                wynik = a / b
            else:
                raise ValueError("Nieznana operacja!")

        except Exception as e:
            print("Wystąpił błąd:", e)
            log_file.write(f"Błąd: {type(e).__name__} - {e}\n")
            log_file.flush()

        else:
            print("Wynik:", wynik)

        finally:
            print("Kolejna operacja...\n")

finally:
    log_file.close() 