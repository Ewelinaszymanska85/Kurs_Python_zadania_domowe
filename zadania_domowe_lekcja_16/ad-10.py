def validate_request(request_dict: dict):
    wymagane_naglowki = ["Host", "User-Agent"]
    naglowki = request_dict.get("headers", {})

    for naglowek in wymagane_naglowki:
        if naglowek not in naglowki:
            raise ValueError(f"Brak wymaganego nagłówka: {naglowek}")

    return "Żądanie poprawne!"


# Test 1 – poprawne żądanie
try:
    wynik = validate_request({
        "method": "GET",
        "target": "/index.html",
        "headers": {
            "Host": "example.com",
            "User-Agent": "PythonClient/1.0"
        }
    })
    print(wynik)
except ValueError as e:
    print(f"BŁĄD: {e}")

# Test 2 – brak Host
try:
    wynik = validate_request({
        "method": "GET",
        "target": "/index.html",
        "headers": {
            "User-Agent": "PythonClient/1.0"
        }
    })
    print(wynik)
except ValueError as e:
    print(f"BŁĄD: {e}")

# Test 3 – brak wszystkich nagłówków
try:
    wynik = validate_request({
        "method": "GET",
        "target": "/index.html",
        "headers": {}
    })
    print(wynik)
except ValueError as e:
    print(f"BŁĄD: {e}") 