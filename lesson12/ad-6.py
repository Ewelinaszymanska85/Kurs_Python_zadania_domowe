class InvalidPasswordError(Exception):
    pass


def ustaw_haslo(haslo):
    if len(haslo) < 8:
        raise InvalidPasswordError("Hasło musi mieć co najmniej 8 znaków.")
    return "Hasło ustawione poprawnie"


# Testowanie
testowe_hasla = [
    "12345",
    "abcdefg",
    "bezpieczne123"
]

for haslo in testowe_hasla:
    try:
        wynik = ustaw_haslo(haslo)
        print(wynik)
    except InvalidPasswordError as e:
        print(f"BŁĄD: {e}")