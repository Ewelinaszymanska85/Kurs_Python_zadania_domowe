sekret = 41

while True:
    liczba = int(input("Zgadnij liczbę: "))

    if liczba == sekret:
        print("Gratulacje! Odgadłeś liczbę.")
        break  # Zakończenie pętli
    else:
        print("To zła liczba. Spróbuj ponownie.") 