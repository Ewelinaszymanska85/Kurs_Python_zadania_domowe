# Resetowanie i przywracanie zmian
## Komendy:

```bash
# Zmiana pliku app.py (Version 1) i dodanie do stagingu
notepad app.py
git add app.py

# Wycofanie zmian z obszaru staging
git reset HEAD app.py

# Sprawdzenie statusu
git status

# Kolejna zmiana app.py i commit
notepad app.py
git add app.py
git commit -m "feat: update hello from python"

# Sprawdzenie historii commitów
git log --oneline

# Cofnięcie do poprzedniego commita (--hard usuwa wszystkie zmiany!)
git reset --hard 9980780
```

## Co robi git reset --hard?
Cofa repozytorium do wskazanego commita i **usuwa wszystkie późniejsze zmiany** – zarówno z plików jak i z historii. Operacja jest nieodwracalna!
