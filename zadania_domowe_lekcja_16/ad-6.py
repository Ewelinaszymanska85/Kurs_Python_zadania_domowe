class HttpRequest:
    """Reprezentuje zadanie HTTP z metoda, celem, naglowkami i trescia (body)."""

    def __init__(self, method, target, headers=None, body=None):
        self.method = method
        self.target = target
        self.headers = headers or {}
        self.body = body or "(empty)"

    def display(self):
        print("--- HTTP Request ---")
        print(f"Method: {self.method}")
        print(f"Target: {self.target}")
        print("Headers:")
        for klucz, wartosc in self.headers.items():
            print(f"  {klucz}: {wartosc}")
        print(f"Body: {self.body}")
        print("-------------------")


if __name__ == "__main__":
    # Test GET
    request1 = HttpRequest(
        method="GET",
        target="/index.html",
        headers={
            "Host": "example.com",
            "User-Agent": "PythonClient/1.0"
        }
    )
    request1.display()

    # Test POST
    request2 = HttpRequest(
        method="POST",
        target="/api/login",
        headers={
            "Host": "example.com",
            "Content-Type": "application/json"
        },
        body='{"username": "Ewelina", "password": "haslo123"}'
    )
    request2.display() 