# Conventional Commits (zaawansowane)
## Komendy:

```bash
# Commity z zakresem (scope)
git commit --allow-empty -m "docs(conflict): dodanie opisu cwiczenia z merge i konfliktow"
git commit --allow-empty -m "feat(conflict): przygotowanie przykladu pracy na branchach"
git commit --allow-empty -m "style(conflict): uporzadkowanie historii commitow"

# Commit z body – szczegółowy opis dlaczego zmiana została wprowadzona
git commit --allow-empty -m "fix(conflict): wyjasnienie procesu rozwiazywania konfliktu merge

Konflikt merge powstaje gdy dwie galęzie modyfikują to samo miejsce w pliku.
Git nie może sam zdecydować która wersja jest właściwa.
Dodano opis kroków rozwiązywania konfliktu aby ułatwić naukę."

# Sprawdzenie historii
git log --oneline
```

## Użyte typy Conventional Commits:
- `feat` – nowa funkcjonalność
- `fix` – poprawka błędu
- `docs` – dokumentacja
- `style` – porządki, formatowanie
- `(conflict)` – zakres (scope) wskazujący którego modułu dotyczy zmiana