# Testy jednostkowe/integracyjne — droga endpoint → DRF → model → baza danych

**Kontekst:** Testy napisane dla realnego projektu dyplomowego NewsHub (agregator
wiadomości RSS, Django + Django REST Framework + PostgreSQL). Zadanie: pokryć
testami każdy element na drodze między wybranym endpointem a bazą danych/modelami.

**Uruchomienie (wewnątrz Dockera, projekt wymaga PostgreSQL):**
```bash
cd NewsHub-PRACA-DYPLOMOWA/newshub
docker compose up -d
docker compose exec web python manage.py test
```

**Wynik: 38 testów, wszystkie przechodzą.**

---

## Wybrany endpoint jako przykład: `POST /api/articles/` (zgłoszenie artykułu)

Droga tego żądania przez warstwy aplikacji:

```
URL (core/urls.py)
   ↓
View: ArticleViewSet.create() (articles/views.py)
   ↓
Permission: IsAuthenticated
   ↓
Serializer: ArticleSerializer (articles/serializers.py) — walidacja danych wejściowych
   ↓
perform_create() — logika biznesowa (wymusza status=PENDING, submitted_by=request.user)
   ↓
Model: Article (articles/models.py) — zapis do bazy danych (PostgreSQL)
   ↓
Signal: post_save → tworzy Notification (articles/signals.py)
```

Każdy z tych elementów ma dedykowany plik testowy, opisany niżej.

---

## Mapowanie plików testowych na elementy drogi

### 1. `test_serializers.py` — warstwa Serializer (izolowana, bez przechodzenia przez cały endpoint)

Testuje `ArticleSerializer` bezpośrednio, w oderwaniu od widoku:
- czy zwraca wszystkie zadeklarowane pola
- czy zagnieżdżone pola (`category_detail`, `tags_detail`) poprawnie serializują
  powiązane obiekty, a nie tylko ich ID
- **czy `read_only_fields` faktycznie blokują ustawienie pól `status`,
  `submitted_by`, `source` przez dane wejściowe** — kluczowy test bezpieczeństwa,
  sprawdzający czy użytkownik nie może sam sobie zatwierdzić artykułu
- czy walidacja wymaganych pól (`title`, `content`) działa na poziomie samego
  serializera

### 2. `test_api.py` i `test_validation.py` — warstwa View/Endpoint

Testują pełną drogę żądania HTTP przez `APIClient`:
- poprawne kody odpowiedzi (200, 404)
- publiczne API pokazuje tylko artykuły ze statusem `APPROVED`
- walidacja na poziomie całego endpointu (brakujące pola, niepoprawny URL)
  — to samo co `test_serializers.py`, ale sprawdzone "z zewnątrz", przez
  rzeczywiste zapytanie HTTP, a nie bezpośrednie wywołanie klasy serializera

### 3. `test_submission.py` — pełny przepływ: endpoint → permission → serializer → model → signal

Testuje cały łańcuch na raz:
- anonimowy użytkownik nie może zgłosić artykułu (401 — permission)
- zalogowany użytkownik może zgłosić artykuł, który zapisuje się ze statusem
  `PENDING` i poprawnym `submitted_by` (cała droga do bazy danych)
- zgłoszenie artykułu **automatycznie** tworzy `Notification` przez sygnał
  `post_save` (element poza głównym przepływem żądanie-odpowiedź)

### 4. `test_models.py` — warstwa Model / baza danych

Testuje bezpośrednio warstwę ORM, bez przechodzenia przez API:
- poprawność tworzenia obiektów i wartości domyślnych (np. `status="PENDING"`)
- metody `__str__`
- sortowanie (`ordering` z klasy `Meta`)

### 5. `sources_tests.py` — warstwa Model / baza danych (ograniczenia integralności)

Testuje model `Source`, w tym ograniczenie na poziomie **samej bazy danych**:
- `unique=True` na polu `rss_url` — próba dodania duplikatu wywołuje
  `IntegrityError` bezpośrednio z warstwy bazy danych, nie z walidacji Django

### 6. `test_auth.py` — warstwa autoryzacji (przed dotarciem do endpointu głównego)

Testuje endpointy Djoser/SimpleJWT, przez które musi przejść użytkownik, zanim
w ogóle uzyska dostęp do zapisu w `/api/articles/`:
- rejestracja, siła hasła (walidacja na poziomie Django `AUTH_PASSWORD_VALIDATORS`)
- logowanie i wydanie tokenu JWT
- odświeżanie tokenu (refresh)

### 7. `test_like.py` — analogiczna droga dla innego endpointu (`/api/articles/<id>/like/`)

Ten sam wzorzec (endpoint → permission → model → baza), zastosowany do innej
funkcjonalności — polubień, w tym ograniczenie `unique_together` na poziomie
modelu `Like` (nie da się polubić tego samego artykułu dwukrotnie).

### 8. `test_admin_moderation.py` — alternatywna "droga" do modelu: przez Django Admin

Pokazuje, że do tego samego modelu `Article` można dotrzeć inną ścieżką niż
REST API — przez panel administracyjny i jego custom actions
(`approve_articles`, `reject_articles`), również przetestowaną end-to-end.

---

## Podsumowanie liczby testów wg elementu drogi

| Element drogi | Plik(i) | Liczba testów |
|---|---|---|
| Model / baza danych | `test_models.py`, `sources_tests.py` | 11 |
| Serializer (izolowany) | `test_serializers.py` | 5 |
| View / Endpoint (przez HTTP) | `test_api.py`, `test_validation.py` | 7 |
| Pełny przepływ + Signal | `test_submission.py` | 3 |
| Autoryzacja (JWT) | `test_auth.py` | 5 |
| Endpoint funkcyjny + logika biznesowa | `test_like.py` | 3 |
| Alternatywna droga (Django Admin) | `test_admin_moderation.py` | 4 |
| **RAZEM** | | **38** |

---

## Wniosek

Testowanie każdego elementu z osobna (Model, Serializer) pozwala szybko
zlokalizować przyczynę błędu — jeśli padnie test na poziomie Serializera,
wiadomo że problem jest w walidacji/reprezentacji danych, a nie np. w logice
widoku czy uprawnieniach. Jednocześnie testy end-to-end (pełny przepływ przez
`APIClient`) potwierdzają, że wszystkie warstwy poprawnie współpracują ze sobą
jako całość — obie perspektywy się uzupełniają.