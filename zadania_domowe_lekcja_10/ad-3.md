# Klonowanie i współpraca
## Komendy:

```bash
# Klonowanie repozytorium z GitHub
git clone https://github.com/Ewelinaszymanska85/Zadanie-domowe--ad-3--GIT-.git

# Wejście do folderu
cd Zadanie-domowe--ad-3--GIT-

# Utworzenie nowej gałęzi
git checkout -b moje-zmiany

# Utworzenie pliku contributors.txt
echo "Ewelina Szymańska" > contributors.txt

# Dodanie do staging i commit
git add contributors.txt
git commit -m "docs: add contributors.txt"

# Wypchnięcie gałęzi na GitHub
git push origin moje-zmiany

# Pull Request na GitHub:
# repozytorium -> zakładka Pull Request -> New pull request
# base: main
# compare: moje-zmiany
# -> Create pull request
```