cena = 100

wiek = int(input("Podaj swój wiek: "))
student = input("Czy jesteś studentem? (tak/nie): ").lower()

if student == "tak" or wiek < 18:
    cena = cena * 0.5       # 50% zniżki

print(f"Cena biletu wynosi {cena} PLN") 