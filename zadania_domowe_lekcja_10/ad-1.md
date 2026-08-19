# Utworzenie folderu i inicjalizacja
mkdir moj-projekt
cd moj-projekt
git init

# Konfiguracja użytkownika (przed pierwszym commitem!)
git config --global user.name "Ewelina"
git config --global user.email "ewelina@gmail.com"

# Utworzenie pliku README z opisem projektu
echo "# Mój Projekt\nTo jest moje pierwsze repozytorium Git." > README.md

# Dodanie do staging i commit
git add README.md
git commit -m "docs: add readme with project description"

# Historia commitów
git log