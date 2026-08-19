def czy_pierwsza(n):
    if n < 2:
        return False 
    for i in range(2, n):
        if n % i == 0: 
            return False 
    return True 

liczby = list(range(1, 31)) 

pierwsze = list(filter(czy_pierwsza, liczby)) 
 
print(pierwsze) 
