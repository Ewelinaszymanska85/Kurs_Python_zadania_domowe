# ============================================================
# Lekcja 22 - Zadanie 7 - Seeder dla Kategorii i Postów
# ============================================================


# ------------------------------------------------------------
# blog/management/commands/seed_blog.py
# (NOWY plik - patrz instrukcja poniżej, jak stworzyć foldery)
# ------------------------------------------------------------
#
# Co robi ta komenda (python manage.py seed_blog):
#
# a) Usuwa WSZYSTKIE istniejące posty i kategorie z bazy danych
#    (Post.objects.all().delete() oraz Category.objects.all().delete())
#    - dzięki temu za każdym uruchomieniem komendy baza jest czysta
#      i nie mnożymy w nieskończoność tych samych danych testowych.
#
# b) Tworzy 8 predefiniowanych kategorii (lista NAZWY_KATEGORII).
#
# c) Tworzy 100 losowych postów za pomocą Faker i każdemu z nich
#    losowo przypisuje jedną z nowo utworzonych kategorii
#    (random.choice(categories)).
#
# ------------------------------------------------------------

import random

from django.core.management.base import BaseCommand
from faker import Faker

from blog.models import Category, Post

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

# Ile losowych postów ma zostać utworzonych.
LICZBA_POSTOW = 100


class Command(BaseCommand):
    help = "Czyści bazę i wypełnia ją przykładowymi kategoriami oraz postami."

    def handle(self, *args, **kwargs):
        # Inicjalizujemy Faker z polską lokalizacją,
        # żeby tytuły i treści postów wyglądały jak polski tekst.
        fake = Faker("pl_PL")

        # ------------------------------------------------------
        # a) Czyszczenie bazy danych
        # ------------------------------------------------------
        # Kolejność ma znaczenie: usuwamy najpierw posty
        # (bo mają ForeignKey do kategorii), a dopiero potem
        # same kategorie. Dzięki temu unikamy problemów z relacjami.
        self.stdout.write("Usuwanie istniejących postów i kategorii...")
        Post.objects.all().delete()
        Category.objects.all().delete()

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
        # c) Tworzenie 100 losowych postów z losową kategorią
        # ------------------------------------------------------
        self.stdout.write("Tworzenie postów...")
        posts = []
        for _ in range(LICZBA_POSTOW):
            post = Post.objects.create(
                title=fake.sentence(nb_words=6),
                content=" ".join(fake.paragraphs(nb=5)),
                # random.choice losuje jedną kategorię z listy
                # utworzonych wcześniej kategorii.
                category=random.choice(categories),
            )
            posts.append(post)

        self.stdout.write(
            self.style.SUCCESS(f"Utworzono {len(posts)} postów.")
        )

        self.stdout.write(self.style.SUCCESS("Seedowanie zakończone pomyślnie!"))