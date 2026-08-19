# Zmienna globalna
POZIOM_DOSTEPU = "user"

def zmien_dostep():
    # Zmienna lokalna o tej samej nazwie (nie zmienia globalnej)
    POZIOM_DOSTEPU = "admin"

    # Wartość wewnątrz funkcji (lokalna)
    print("Wewnątrz funkcji:", POZIOM_DOSTEPU)

# Wywołanie funkcji
zmien_dostep()

# Wartość na zewnątrz funkcji (globalna)
print("Na zewnątrz funkcji:", POZIOM_DOSTEPU) 