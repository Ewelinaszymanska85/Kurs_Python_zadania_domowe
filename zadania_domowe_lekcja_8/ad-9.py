try:
    with open("dane.txt", "r") as plik:
        print(plik.read())

except FileNotFoundError:
    print("Plik nie istnieje.") 
    