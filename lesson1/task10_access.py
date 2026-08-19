wzrost = int(input("Podaj wzrost w cm: "))
opiekun = input("Czy jest opiekun? (tak/nie): ")

mozna_wejsc = (wzrost >= 120 and opiekun == "tak") or wzrost >= 160

print(mozna_wejsc)