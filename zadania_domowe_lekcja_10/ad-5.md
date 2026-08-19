# Praca z plikami i commitami
## Plik app.py:

```python
def hello_world():
    print("Hello, World!")

hello_world()
```

## Komendy:

```bash
# Utworzenie pliku app.py
notepad app.py

# Dodanie do staging i pierwszy commit
git add app.py
git commit -m "feat: add hello world function"

# Modyfikacja pliku (zmiana komunikatu)
notepad app.py

# Sprawdzenie statusu
git status

# Dodanie zmian i drugi commit
git add app.py
git commit -m "fix: update hello world message"
```