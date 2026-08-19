class BladWalidacjiError(Exception): 
    def __init__(self, bledy): 
        self.bledy = bledy 
        super().__init__("\n".join(bledy)) 
        
def waliduj_haslo(haslo): 
    bledy = [] 
    
    if len(haslo) < 8: 
        bledy.append("Hasło musi mieć min. 8 znaków.") 
        
    if not any(c.islower() for c in haslo): 
        bledy.append("Brak małej litery.") 
        
    if not any(c.isupper() for c in haslo): 
        bledy.append("Brak dużej litery.") 
        
    if not any(c.isdigit() for c in haslo):
        bledy.append("Brak cyfr.")
        
    if not any(c in "!@#$%^&*()-_=+[]{};:,.<>?/\\|" for c in haslo):
        bledy.append("Brak znaku specjalnego.") 
        
    if bledy:
        raise BladWalidacjiError(bledy) 
    
    return [] 


try: 
    haslo = input("Podaj hasło: ") 
    waliduj_haslo(haslo) 
    print("Hasło poprawne") 
except BladWalidacjiError as e: 
    print("Błedy walidacji:") 
    for blad in e.bledy: 
        print("-", blad) 