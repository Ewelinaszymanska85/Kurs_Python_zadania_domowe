def sprawdz_haslo(haslo: str) -> bool:
    """
    Sprawdza, czy hasło spełnia podstawowe wymagania bezpieczeństwa.

    Hasło jest uznawane za poprawne, jeśli:
    - ma co najmniej 8 znaków,
    - zawiera co najmniej jedną wielką literę,
    - zawiera co najmniej jedną cyfrę.

    Parametry:
    haslo (str): hasło podane przez użytkownika

    Zwraca:
    bool: True jeśli hasło spełnia wszystkie warunki, False w przeciwnym razie
    """

    if len(haslo) < 8:
        return False

    ma_wielka = any(znak.isupper() for znak in haslo)
    ma_cyfre = any(znak.isdigit() for znak in haslo)

    return ma_wielka and ma_cyfre


print(sprawdz_haslo("hgf"))          # False
print(sprawdz_haslo("Lhbdky99"))     # True
print(sprawdz_haslo("ldibsc1"))     # False