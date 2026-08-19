def oblicz_srednia(*args):
    # Jeśli nie podano żadnych ocen, zwracamy 0
    if len(args) == 0:
        return 0

    return sum(args) / len(args)


print(oblicz_srednia(5, 4, 3, 6))  
print(oblicz_srednia(2, 5))        
print(oblicz_srednia())            