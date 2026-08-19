a = float(input("Podaj pierwszą liczbę:")) 
b = float(input("Podaj drugą liczbę:")) 
znak = input("Podaj znak(+,-,*,/):") 

if znak =="+": 
    print("Wynik:",a + b) 
elif znak =="-":
    print("Wynik:",a - b) 
elif znak =="*":
    print("Wynik:",a*b)
elif znak =="/": 
    print("Wynik:",a/b)
else:
    print("Nieznana operacja")  
    