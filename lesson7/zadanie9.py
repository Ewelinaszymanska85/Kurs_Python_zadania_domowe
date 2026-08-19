def powtorz(n):
    def dekorator(funkcja):
        def wrapper():
            for i in range(n):
                funkcja()
        
        return wrapper
    
    return dekorator


@powtorz(4)
def przywitaj():
    print("Cześć!")


przywitaj() 