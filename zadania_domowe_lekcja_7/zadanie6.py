def stworz_licznik():
    licznik = 0 
    
    def zwieksz():
        nonlocal licznik 
        licznik += 1 
        return licznik 
    
    return zwieksz 

licz = stworz_licznik() 

print(licz()) 
print(licz()) 
print(licz()) 