# Rebase i interaktywna edycja historii
## Komendy:

```bash
# Ustawienie VS Code jako edytora git
git config --global core.editor "code --wait"

# Utworzenie gałęzi feature-branch
git checkout master
git checkout -b feature-branch

# Trzy oddzielne commity
notepad app.py
git add app.py
git commit -m "chore: first change"

notepad app.py
git add app.py
git commit -m "chore: second change"

notepad app.py
git add app.py
git commit -m "chore: third change"

# Interaktywny rebase – połączenie 3 commitów w 1
git rebase -i HEAD~3

# W VS Code który się otworzy:
# - pierwszą linię zostawić jako "pick"
# - pozostałe dwie zmienić z "pick" na "squash"
# - zapisać i zamknąć plik (Ctrl+S, potem zamknąć kartę)
# - w kolejnym oknie wpisać nowy komunikat:
#   feat: add combined feature changes
# - zapisać i zamknąć

# Wypchnięcie na GitHub (--force bo zmieniliśmy historię)
git push --force origin feature-branch
```