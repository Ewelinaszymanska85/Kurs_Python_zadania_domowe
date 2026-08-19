wiek = int(input("Podaj swój wiek: "))


if 0 <= wiek <= 1:
    print("Niemowlę")
elif 2 <= wiek <= 12:
    print("Dziecko")
elif 13 <= wiek <= 17:
    print("Nastolatek")
elif 18 <= wiek <= 64:
    print("Dorosły")
elif wiek >= 65:
    print("Senior")
else:
    print("Podano nieprawidłowy wiek.") 