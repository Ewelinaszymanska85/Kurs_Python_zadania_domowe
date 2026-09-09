# Lekcja 33 — Testy projektu NewsHub

Zadanie domowe z lekcji 33 zostało zaktualizowane na podstawie aktualnej wersji projektu dyplomowego NewsHub.

Celem zestawu jest pokazanie testowania różnych warstw aplikacji: modeli, serializerów, endpointów REST API, logiki biznesowej, moderacji, polubień, źródeł RSS, scraperów oraz automatycznej kategoryzacji.

## Mapowanie plików testowych na warstwy aplikacji

### 1. `test_serializers.py` — warstwa Serializer

Testy sprawdzają `ArticleSerializer` bezpośrednio, bez przechodzenia przez cały endpoint.

Zakres obejmuje m.in.:

- poprawność serializacji pól artykułu,
- walidację danych wejściowych,
- pola wymagane,
- relacje z kategoriami i tagami,
- zachowanie pól tylko do odczytu,
- ochronę pól sterowanych przez backend,
- poprawność danych zwracanych przez serializer.

Liczba testów: **11**

### 2. `test_api.py` — warstwa REST API

Testy sprawdzają publiczne API artykułów przez `APIClient`.

Zakres:

- poprawność odpowiedzi endpointu,
- filtrowanie danych widocznych publicznie,
- zachowanie endpointu zgodnie z aktualną logiką aplikacji.

Liczba testów: **1**

### 3. `test_validation.py` — walidacja danych

Testy sprawdzają walidację danych przesyłanych do aplikacji.

Zakres obejmuje:

- brak wymaganych pól,
- niepoprawne dane,
- walidację tytułu,
- walidację treści artykułu.

Liczba testów: **4**

### 4. `test_submission.py` — pełny przepływ zgłaszania artykułu

Testy sprawdzają cały proces zgłoszenia artykułu:

`request -> permission -> serializer -> model -> database -> signal`

Zakres:

- brak dostępu dla użytkownika anonimowego,
- możliwość zgłoszenia artykułu przez użytkownika zalogowanego,
- zapis artykułu ze statusem `PENDING`,
- powiązanie artykułu z użytkownikiem,
- automatyczne utworzenie powiadomienia przez sygnał Django.

Liczba testów: **3**

### 5. `test_models.py` — warstwa Model / ORM

Testy sprawdzają zachowanie modeli bezpośrednio na poziomie Django ORM.

Zakres:

- tworzenie obiektów,
- wartości domyślne,
- metody modelu,
- zachowanie danych zapisanych w bazie.

Liczba testów: **2**

### 6. `sources_tests.py` — źródła RSS i logika biznesowa

To największa grupa testów w zestawie.

Sprawdzane są m.in.:

- tworzenie źródła RSS,
- unikalność `rss_url`,
- domyślna aktywność źródła,
- sortowanie źródeł,
- poziomy zaufania `TRUSTED`, `NORMAL`, `BLOCKED`,
- określanie statusu artykułu,
- blokowanie nieaktywnych i zablokowanych źródeł,
- pobieranie artykułów z RSS,
- tworzenie artykułów ze statusem `APPROVED` lub `PENDING`,
- obsługa daty publikacji,
- fallback z `published` do `updated`.

Liczba testów: **20**

### 7. `test_like.py` — logika polubień

Testy sprawdzają endpoint:

`/api/articles/<id>/like/`

Zakres:

- użytkownik anonimowy nie może polubić artykułu,
- użytkownik zalogowany może dodać polubienie,
- ponowne wywołanie endpointu usuwa polubienie,
- poprawność zmian w bazie danych.

Liczba testów: **3**

### 8. `test_admin_moderation.py` — moderacja przez Django Admin

Testy sprawdzają custom actions w panelu administracyjnym.

Zakres:

- zatwierdzanie artykułów,
- odrzucanie artykułów,
- poprawność zmiany statusu obiektu.

Liczba testów: **3**

### 9. `test_categorization.py` — automatyczna kategoryzacja artykułów

Testy sprawdzają logikę automatycznego przypisywania kategorii.

Zakres obejmuje:

- wybór kategorii na podstawie treści,
- obsługę wyniku AI,
- mechanizm fallback,
- zachowanie przy braku poprawnej odpowiedzi,
- poprawność normalizacji danych.

Liczba testów: **7**

### 10. `test_scrapers.py` — scrapery artykułów

Testy sprawdzają logikę pobierania danych z obsługiwanych serwisów.

Zakres:

- rozpoznawanie obsługiwanych domen,
- odrzucanie nieobsługiwanej domeny,
- ekstrakcję tytułu i treści,
- obsługę brakujących danych,
- wybór odpowiedniego scrapera,
- pobranie strony i przekazanie danych do parsera.

Liczba testów: **6**

### 11. `test_url_import.py` — import artykułu z adresu URL

Testy sprawdzają endpoint importujący dane artykułu z podanego adresu URL.

Zakres:

- poprawne żądanie,
- walidację URL,
- obsługę nieobsługiwanej domeny,
- pobieranie danych przez scraper,
- integrację z automatyczną kategoryzacją.

Liczba testów: **5**

---

## Podsumowanie liczby testów

| Plik | Liczba testów |
|---|---:|
| `sources_tests.py` | 20 |
| `test_admin_moderation.py` | 3 |
| `test_api.py` | 1 |
| `test_categorization.py` | 7 |
| `test_like.py` | 3 |
| `test_models.py` | 2 |
| `test_scrapers.py` | 6 |
| `test_serializers.py` | 11 |
| `test_submission.py` | 3 |
| `test_url_import.py` | 5 |
| `test_validation.py` | 4 |
| **RAZEM** | **65** |

## Wniosek

Testowanie poszczególnych warstw aplikacji pozwala szybko określić miejsce wystąpienia błędu.

Testy modeli i serializerów sprawdzają pojedyncze elementy systemu w izolacji, natomiast testy wykonywane przez `APIClient` potwierdzają współpracę wielu warstw aplikacji jednocześnie.

Dodatkowe testy logiki RSS, scraperów, importu URL i automatycznej kategoryzacji sprawdzają własną logikę biznesową projektu NewsHub.

Zestaw z lekcji 33 zawiera obecnie **65 testów**, natomiast pełny projekt NewsHub przechodzi **68 testów**.