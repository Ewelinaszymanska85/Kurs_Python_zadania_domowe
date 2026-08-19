"""
Pomocniczy skrypt - tworzy 100 małych plików testowych na potrzeby
Zadania 16.
"""

import os

folder = "pliki_testowe"
os.makedirs(folder, exist_ok=True)

for i in range(1, 101):
    with open(f"{folder}/plik_{i}.txt", "w") as f:
        f.write(f"To jest zawartość pliku numer {i}")

print("Utworzono 100 plików testowych w folderze 'pliki_testowe'.") 


# Uruchom: python stwotz_pliki_testowe.py 