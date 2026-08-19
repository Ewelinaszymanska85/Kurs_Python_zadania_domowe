zdanie = input("Podaj zdanie: ")

# Przetwarzanie każdego znaku w zdaniu
for litera in zdanie:
    # Pomijanie znaków, które nie są samogłoskami
    if litera.lower() not in "aeiouy":
        continue

    print(litera) 