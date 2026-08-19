# Rozwiązywanie konfliktów w Git
## Komendy:

```bash
# Inicjalizacja repozytorium
mkdir git-conflict-zadanie
cd git-conflict-zadanie
git init
git checkout -b main

# Pierwsza linia i commit
echo "Linia 1 - wersja glowna" > conflict_example.txt
git add conflict_example.txt
git commit -m "feat: dodano pierwsza linie"

# Gałąź branch-A – edycja pliku
git checkout -b branch-A
echo "Linia 2 - z branch-A" >> conflict_example.txt
git add conflict_example.txt
git commit -m "feat: dodano druga linie w branch-A"

# Powrót na main – inna edycja tego samego miejsca
git checkout main
echo "Linia 1 zmieniona w main" > conflict_example.txt
echo "Linia 2 - z main" >> conflict_example.txt
git add conflict_example.txt
git commit -m "fix: zmieniono pierwsza linie i dodano druga w main"

# Merge – tu powstaje konflikt!
git merge branch-A
```

## Rozwiązanie konfliktu:
Po `git merge branch-A` git zgłosi konflikt w pliku `conflict_example.txt`.
Otworzyć plik i ręcznie wybrać właściwą wersję — usunąć znaczniki `<<<<<<<`, `=======`, `>>>>>>>`.

```bash
# Po ręcznym rozwiązaniu konfliktu
git add conflict_example.txt
git commit -m "fix: rozwiazano konflikt merge branch-A"
```

## Czego nauczyło mnie to zadanie:
Konflikt powstaje gdy dwie gałęzie modyfikują **to samo miejsce** w pliku.
Git nie może sam zdecydować która wersja jest właściwa — trzeba to zrobić ręcznie.