prawo_jazdy = input("Czy masz prawo jazdy? (tak/nie): ")
wiek = int(input("Ile masz lat?: "))

wynik = (prawo_jazdy.lower() == "tak") and (wiek >= 18)

print(wynik) 