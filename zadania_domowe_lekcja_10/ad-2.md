```bash
# Sprawdzenie gałęzi
git branch

# Zmiana nazwy z master na main
git branch -M main

# Utworzenie gałęzi feature-login
git branch feature-login

# Przełączenie na nową gałąź
git checkout feature-login

# Utworzenie pliku login.py
echo "print('Logowanie użytkownika')" > login.py

# Dodanie do staging i commit
git add login.py
git commit -m "feat: add login.py"

# Powrót na main
git checkout main

# Scalenie gałęzi
git merge feature-login
git branch -d feature-login

# Sprawdzenie historii
git log
```