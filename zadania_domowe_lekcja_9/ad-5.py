import csv

produkty = [
    {"nazwa": "Mleko", "cena": 3.50},
    {"nazwa": "Chleb", "cena": 4.20}
]

with open("produkty.csv", "w", newline="", encoding="utf-8") as plik:
    pola = ["nazwa", "cena"]
    writer = csv.DictWriter(plik, fieldnames=pola)

    writer.writeheader()
    writer.writerows(produkty)

print("Dane zapisane do pliku produkty.csv") 