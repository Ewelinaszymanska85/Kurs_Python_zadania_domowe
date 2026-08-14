"""
Zadanie 4 - Utworzenie pliku .dockerignore

============================================================
PLIK .dockerignore (główny katalog projektu)
============================================================

venv/
__pycache__/
*.pyc
db.sqlite3
.env
.git/
.gitignore
*.log
zadania domowe docker/

============================================================
UZASADNIENIE WYBORU WYKLUCZONYCH PLIKÓW
============================================================

- venv/          - środowisko wirtualne jest ogromne i całkowicie
                   zbędne w obrazie; Docker instaluje zależności
                   niezależnie, przez requirements.txt
- __pycache__/,
  *.pyc          - skompilowane pliki bytecode Pythona, generują
                   się automatycznie przy uruchomieniu, nie mają
                   sensu jako część obrazu
- db.sqlite3     - dane, nie kod - baza danych nie powinna trafiać
                   do obrazu (a już na pewno nie do rejestru obrazów)
- .env           - plik z sekretami (SECRET_KEY, hasła). Wrzucenie
                   go do obrazu Docker byłoby poważnym błędem
                   bezpieczeństwa, zwłaszcza jeśli obraz trafi
                   kiedyś do publicznego/prywatnego rejestru
- .git/          - cała historia commitów repozytorium, kompletnie
                   niepotrzebna w działającej aplikacji
- zadania domowe
  docker/        - dokumentacja zadań na potrzeby kursu, nie jest
                   częścią samej aplikacji

============================================================
WYNIKI PRZED / PO
============================================================

Porównanie rozmiaru obrazu zbudowanego BEZ .dockerignore (v1)
i PO jego dodaniu (v2):

    django-docker-demo:v1  (bez .dockerignore): 349 MB (70.3 MB content)
    django-docker-demo:v2  (z .dockerignore):   260 MB (56.1 MB content)

Redukcja rozmiaru obrazu o ok. 90 MB - potwierdzona wynikiem
komendy `docker images`.

============================================================
WNIOSEK
============================================================

Plik .dockerignore działa analogicznie do .gitignore, ale
dotyczy kontekstu budowania obrazu Docker (docker build), a nie
repozytorium Git. Poza oszczędnością miejsca, jego kluczową rolą
jest bezpieczeństwo - zapobiega przypadkowemu "wpieczeniu" plików
z sekretami (jak .env) do finalnego obrazu, który mógłby zostać
udostępniony w rejestrze Docker Hub lub prywatnym.
""" 