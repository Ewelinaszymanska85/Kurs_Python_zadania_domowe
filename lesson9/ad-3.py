import json 

konfiguracja = {
    "uzytkownik": "admin", 
    "motyw": "ciemny", 
    "rozdzielczosc": [1920, 1080] 
    }

with open("config.json", "w", encoding="utf-8") as plik: 
    json.dump(konfiguracja, plik, ensure_ascii=False, indent=4) 
    
print("Konfiguracja została zapisana do pliku config.json") 