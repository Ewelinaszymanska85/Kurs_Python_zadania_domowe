# ============================================================
# Lekcja 22 - Zadanie 5 - Testowanie Fakera
# ============================================================
#
# Prosty, samodzielny skrypt (poza projektem Django), który
# importuje bibliotekę Faker i drukuje w konsoli:
# - 10 losowych polskich imion i nazwisk,
# - 10 losowych zdań.
#
# Uruchomienie (w aktywnym wirtualnym środowisku z zainstalowanym
# Fakerem - patrz Zadanie 4):
#
#   python test_faker.py
#
# ============================================================

from faker import Faker

# Inicjalizujemy Faker z polską lokalizacją (pl_PL),
# dzięki czemu generowane dane będą wyglądały jak polskie
# imiona, nazwiska i zdania, a nie np. angielskie.
fake = Faker("pl_PL")

print("=== 10 losowych polskich imion i nazwisk ===")
for _ in range(10):
    print(fake.name())

print()

print("=== 10 losowych zdań ===")
for _ in range(10):
    print(fake.sentence()) 