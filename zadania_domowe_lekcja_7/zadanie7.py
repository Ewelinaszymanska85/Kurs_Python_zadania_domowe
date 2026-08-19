def loguj(funkcja):
    def wrapper():
        print(f"Uruchamiam funkcję {funkcja.__name__}...")
        
        funkcja()
        
        print(f"Zakończono funkcję {funkcja.__name__}.")
    
    return wrapper


@loguj
def przywitaj():
    print("Witaj!")


przywitaj()