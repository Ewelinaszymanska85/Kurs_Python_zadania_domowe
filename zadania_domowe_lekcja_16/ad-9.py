import requests
import json

# Oryginalny zasób na serwerze /users/1
zasob = {
    "name": "Katarzyna",
    "email": "k.nowak@example.com",
    "city": "Warszawa"
}

URL = "https://example.com/api/users/1"

# PUT – zastępuje CAŁY zasób, trzeba wysłać wszystkie pola,
# bo pominięte pola zostałyby usunięte/wyzerowane
put_body = {
    "name": "Kasia",
    "email": "k.nowak@example.com",
    "city": "Warszawa"
}
# response = requests.put(URL, json=put_body)

# PATCH – aktualizuje TYLKO podane pola, reszta zasobu zostaje bez zmian
patch_body = {
    "name": "Kasia"
}
# response = requests.patch(URL, json=patch_body)

print("Zasób oryginalny:", zasob)
print("PUT body:        ", put_body)
print("PATCH body:      ", patch_body)

# Porównanie ilości przesyłanych danych
rozmiar_put = len(json.dumps(put_body))
rozmiar_patch = len(json.dumps(patch_body))

print(f"\nLiczba pól PUT:   {len(put_body)} | rozmiar: {rozmiar_put} znaków")
print(f"Liczba pól PATCH: {len(patch_body)} | rozmiar: {rozmiar_patch} znaków")
print(f"PATCH jest mniejszy o {rozmiar_put - rozmiar_patch} znaków")

# PUT jest idempotentny i zastępuje cały zasób – wymaga przesłania
# wszystkich pól, nawet niezmienionych.
# PATCH przesyła tylko zmienione pola – jest bardziej "oszczędny"
# pod względem ilości danych, zwłaszcza przy dużych zasobach. 