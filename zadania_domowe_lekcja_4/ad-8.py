wiek_psa = int(input("Podaj wiek psa w latach: "))

if wiek_psa <= 0:
    print("Wiek psa musi być większy od zera.")
elif wiek_psa == 1:
    ludzki_wiek = 15
elif wiek_psa == 2:
    ludzki_wiek = 15 + 9
else:
    ludzki_wiek = 15 + 9 + (wiek_psa - 2) * 5

print("Wiek psa w ludzkich latach wynosi:", ludzki_wiek) 