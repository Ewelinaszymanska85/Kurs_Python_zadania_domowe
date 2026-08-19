uzytkownicy = [ 
    {"imie": "Jan", "wiek": 30, "aktywny": True},
    {"imie": "Anna", "wiek": 17, "aktywny": False},
    {"imie": "Piotr", "wiek": 25, "aktywny": True}
] 

wynik = [u["imie"].upper() for u in uzytkownicy if u["aktywny"] and u["wiek"] >= 18] 

print(wynik) 