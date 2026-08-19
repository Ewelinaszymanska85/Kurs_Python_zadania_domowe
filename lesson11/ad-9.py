class RejestracjaUzytkownika:
    def __init__(self, email, haslo):
        if "@" not in email:
            raise ValueError("Niepoprawny email – brak znaku '@'.")
        if len(haslo) < 8:
            raise ValueError("Hasło musi mieć co najmniej 8 znaków.")

        self.email = email
        self.haslo = haslo


# Testowanie z try...except
dane_testowe = [
    ("alamail.com", "12345678"),      # brak @
    ("ala@mail.com", "123"),          # za krótkie hasło
    ("asia@mail.com", "bezpieczne1")  # poprawne
]

for email, haslo in dane_testowe:
    try:
        user = RejestracjaUzytkownika(email, haslo)
        print(f"OK: utworzono konto dla {user.email}")
    except ValueError as e:
        print(f"BŁĄD: {e}")