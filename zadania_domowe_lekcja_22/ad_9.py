# ============================================================
# Lekcja 22 - Zadanie 9 - Rozbudowa Seedera o Tagi
# ============================================================


# ------------------------------------------------------------
# blog/management/commands/seed_blog.py
# (CAŁY PLIK - zastąp obecną zawartość tą wersją)
#
# Co się zmieniło względem Zadania 7:
# - dodajemy listę predefiniowanych tagów i tworzymy je w bazie
#   (podobnie jak kategorie),
# - w pętli czyszczącej bazę dodajemy też usuwanie starych tagów,
# - po stworzeniu każdego posta losujemy od 1 do 5 tagów z listy
#   dostępnych tagów i przypisujemy je do posta metodą
#   post.tags.set(...).
#
# Dlaczego używamy .set(), a nie .add()?
# - .set(lista_tagów) nadpisuje CAŁĄ listę tagów posta za jednym
#   razem - idealne przy tworzeniu nowego posta od zera.
# - .add(tag1, tag2, ...) DOKŁADA pojedyncze tagi do istniejącej
#   listy, bez usuwania poprzednich - przydatne raczej przy
#   edycji istniejącego posta.
#
# Dlaczego random.sample(), a nie kilka razy random.choice()?
# - random.sample(lista, k) losuje k RÓŻNYCH elementów z listy
#   (bez powtórzeń). Gdybyśmy użyli random.choice() w pętli,
#   ten sam tag mógłby zostać wylosowany kilka razy dla jednego
#   posta, co nie ma sensu (post nie powinien mieć zduplikowanego
#   tego samego tagu).
# ------------------------------------------------------------

import random

from django.core.management.base import BaseCommand
from faker import Faker

from blog.models import Category, Post, Tag

# Lista predefiniowanych kategorii do stworzenia w bazie.
NAZWY_KATEGORII = [
    "Technologia",
    "Podróże",
    "Kulinaria",
    "Sport",
    "Zdrowie",
    "Muzyka",
    "Film",
    "Nauka",
]

# Lista predefiniowanych tagów do stworzenia w bazie.
NAZWY_TAGOW = [
    "Python",
    "Django",
    "Backend",
    "Frontend",
    "AI",
    "Poradnik",
    "Nowości",
    "Recenzja",
    "Wskazówki",
    "Wydarzenia",
    "Bezpieczeństwo",
    "Wydajność",
]

# Ile losowych postów ma zostać utworzonych.
LICZBA_POSTOW = 100

# Zakres liczby tagów losowo przypisywanych do jednego posta.
MIN_TAGOW_NA_POST = 1
MAX_TAGOW_NA_POST = 5


class Command(BaseCommand):
    help = (
        "Czyści bazę i wypełnia ją przykładowymi kategoriami, "
        "tagami oraz postami z losowo przypisanymi tagami."
    )

    def handle(self, *args, **kwargs):
        fake = Faker("pl_PL")

        # ------------------------------------------------------
        # a) Czyszczenie bazy danych
        # ------------------------------------------------------
        # Kolejność: najpierw posty (mają FK do Category i M2M
        # do Tag), potem kategorie i tagi.
        self.stdout.write("Usuwanie istniejących postów, kategorii i tagów...")
        Post.objects.all().delete()
        Category.objects.all().delete()
        Tag.objects.all().delete()

        # ------------------------------------------------------
        # b) Tworzenie predefiniowanych kategorii
        # ------------------------------------------------------
        self.stdout.write("Tworzenie kategorii...")
        categories = []
        for nazwa in NAZWY_KATEGORII:
            category = Category.objects.create(name=nazwa)
            categories.append(category)

        self.stdout.write(
            self.style.SUCCESS(f"Utworzono {len(categories)} kategorii.")
        )

        # ------------------------------------------------------
        # c) Tworzenie predefiniowanych tagów
        # ------------------------------------------------------
        self.stdout.write("Tworzenie tagów...")
        tags = []
        for nazwa in NAZWY_TAGOW:
            tag = Tag.objects.create(name=nazwa)
            tags.append(tag)

        self.stdout.write(
            self.style.SUCCESS(f"Utworzono {len(tags)} tagów.")
        )

        # ------------------------------------------------------
        # d) Tworzenie 100 losowych postów z losową kategorią
        #    oraz losowym zestawem od 1 do 5 tagów
        # ------------------------------------------------------
        self.stdout.write("Tworzenie postów...")
        posts = []
        for _ in range(LICZBA_POSTOW):
            post = Post.objects.create(
                title=fake.sentence(nb_words=6),
                content=" ".join(fake.paragraphs(nb=5)),
                category=random.choice(categories),
            )

            # Losujemy, ile tagów dostanie ten post (od 1 do 5).
            liczba_tagow = random.randint(MIN_TAGOW_NA_POST, MAX_TAGOW_NA_POST)

            # Losujemy konkretne, różne tagi z pełnej listy tagów.
            wylosowane_tagi = random.sample(tags, k=liczba_tagow)

            # .set() przypisuje postowi całą listę tagów naraz -
            # to standardowy sposób ustawiania relacji ManyToMany.
            post.tags.set(wylosowane_tagi)

            posts.append(post)

        self.stdout.write(
            self.style.SUCCESS(f"Utworzono {len(posts)} postów z losowymi tagami.")
        )

        self.stdout.write(self.style.SUCCESS("Seedowanie zakończone pomyślnie!")) 