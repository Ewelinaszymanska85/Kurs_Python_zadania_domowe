# BeatHub — Wstępna dokumentacja projektu
### Projekt końcowy kursu Python/Django — Lekcja 28

---

## 1. Discovery / Definicja produktu

BeatHub to portal muzyczny, na którym użytkownicy mogą odkrywać artystów, albumy i
piosenki, a także tworzyć własne, publiczne playlisty. W odróżnieniu od prostego katalogu
"tylko do odczytu", katalog jest współtworzony przez społeczność — zalogowani użytkownicy
mogą dodawać nowych artystów, albumy i piosenki, a nie tylko przeglądać treści wprowadzone
przez administratora.

**Priorytety:**
- Odkrywanie muzyki przez przeglądanie i filtrowanie (artysta / album / gatunek)
- Tworzenie i zarządzanie własnymi playlistami
- Publiczna widoczność wszystkich playlist i profili — element społecznościowy

---

## 2. Założenia architektoniczne

- Aplikacja webowa oparta o Django (backend) + Django REST Framework (API)
- Model danych relacyjny (PostgreSQL lub SQLite na etapie developmentu)
- Uwierzytelnianie wbudowane w Django (`django.contrib.auth`)
- Wszystkie playlisty są **publiczne** — nie ma trybu prywatnego (uproszczenie na tym etapie)
- Katalog (artyści/albumy/piosenki) jest **współtworzony przez użytkowników**, nie tylko
  przez administratora — wymaga to podstawowej kontroli uprawnień (kto może edytować/usuwać
  wpisy, które sam dodał, vs uprawnienia admina do zarządzania całością)
- Bez odtwarzania rzeczywistego dźwięku (brak plików audio) — projekt skupia się na
  metadanych i organizacji treści, a nie na streamingu

---

## 3. User Stories (Wymagania użytkownika)

- Jako **gość**, chcę przeglądać artystów, albumy i piosenki, aby odkrywać nową muzykę bez
  konieczności zakładania konta.
- Jako **gość**, chcę przeglądać publiczne playlisty innych użytkowników, aby inspirować się
  ich wyborem muzyki.
- Jako **zalogowany użytkownik**, chcę dodać nowego artystę/album/piosenkę do katalogu, aby
  rozbudować bazę o brakujące pozycje.
- Jako **zalogowany użytkownik**, chcę tworzyć własne playlisty i dodawać do nich piosenki,
  aby organizować muzykę według własnych preferencji.
- Jako **zalogowany użytkownik**, chcę ustalać kolejność piosenek w mojej playliście, aby
  kontrolować sposób jej odtwarzania.
- Jako **zalogowany użytkownik**, chcę edytować lub usuwać własne playlisty oraz wpisy
  katalogu, które sam dodałem, aby poprawiać błędy.
- Jako **użytkownik**, chcę mieć publiczny profil z moimi playlistami, aby inni mogli je
  zobaczyć.

---

## 4. Specyfikacja funkcjonalna

- Przeglądanie katalogu: lista artystów, lista albumów danego artysty, lista piosenek
  danego albumu
- Filtrowanie/wyszukiwanie: po gatunku, po artyście, po tytule piosenki
- Rejestracja, logowanie, wylogowanie (`django.contrib.auth`)
- Dodawanie nowego artysty / albumu / piosenki przez zalogowanego użytkownika
  (z walidacją danych wejściowych i odpowiednimi komunikatami błędów)
- Tworzenie, edycja i usuwanie playlist (tylko przez właściciela playlisty)
- Dodawanie / usuwanie piosenek z playlisty, z możliwością ustalenia kolejności
  (niestandardowa tabela pośrednia `through`)
- Publiczny profil użytkownika z listą jego playlist
- Panel administracyjny z rozszerzonym `list_display`, `search_fields`, `list_filter`
  oraz `inlines` (np. edycja piosenek albumu bezpośrednio z poziomu albumu w adminie)
- Generowanie danych testowych komendą `manage.py seed_db` (Faker)
- Testy jednostkowe kluczowych funkcjonalności (tworzenie modeli, dostępność widoków,
  poprawność kodów odpowiedzi HTTP)

---

## 5. Model domenowy (Domain Model)

**Główne encje i relacje:**

- **Gatunek** (`Genre`) — nazwa gatunku muzycznego
- **Artysta** (`Artist`) — pseudonim/nazwa, zdjęcie; powiązany z gatunkiem (`ManyToMany`,
  bo artysta może tworzyć w wielu gatunkach)
- **Album** (`Album`) — tytuł, data wydania, okładka; należy do jednego artysty
  (`ForeignKey`)
- **Piosenka** (`Song`) — tytuł, czas trwania; należy do jednego albumu (`ForeignKey`),
  opcjonalnie własny gatunek jeśli różni się od albumu
- **Playlista** (`Playlist`) — nazwa, opis, właściciel (`ForeignKey` do `User`), publiczna
  z założenia
- **PlaylistSong** (tabela pośrednia `through`) — łączy `Playlist` i `Song`, dodatkowo
  przechowuje **pozycję/kolejność** piosenki na playliście (pole `order`)
- **Użytkownik** (`User`) — wbudowany model Django; autor wpisów katalogu i playlist

**Relacje:**
- Artysta ←→ Gatunek: `ManyToMany`
- Artysta → Album: `OneToMany` (jeden artysta, wiele albumów)
- Album → Piosenka: `OneToMany` (jeden album, wiele piosenek)
- Playlista ←→ Piosenka: `ManyToMany` przez własną tabelę pośrednią `PlaylistSong`
  (przechowuje kolejność)
- Użytkownik → Playlista: `OneToMany` (jeden użytkownik, wiele playlist)
- Użytkownik → Artysta/Album/Piosenka: pole `added_by` (`ForeignKey` do `User`) —
  do kontroli uprawnień edycji/usuwania

---

## 6. Plan działania (Roadmap)

### 6.1 MVP — rdzeń aplikacji
- Modele: Gatunek, Artysta, Album, Piosenka, Playlista, PlaylistSong
- Rejestracja / logowanie / wylogowanie
- Przeglądanie katalogu (listy + szczegóły)
- Tworzenie playlisty i dodawanie do niej piosenek (bez reorderowania na start)
- Podstawowy panel admina

### 6.2 V1.0 — organizacja i społeczność
- Dodawanie artystów/albumów/piosenek przez użytkowników (z walidacją)
- Reorder piosenek na playliście (wykorzystanie pola `order` w `PlaylistSong`)
- Wyszukiwanie i filtrowanie katalogu (po gatunku, artyście)
- Publiczne profile użytkowników z listą playlist
- Rozszerzony panel admina (`inlines`, `search_fields`, `list_filter`)

### 6.3 V1.5+ — jakość i utrzymanie
- Testy jednostkowe i integracyjne (modele, widoki, walidacja)
- Komenda `seed_db` z danymi testowymi (Faker)
- Obsługa błędów i komunikatów walidacji (np. próba dodania playlisty bez nazwy)
- Estetyczny interfejs, obsługa dostępu niezalogowanych użytkowników do stron wymagających
  logowania

---

## Uwagi końcowe

Ten dokument stanowi wstępny plan — szczegóły pól modeli, dokładne endpointy API oraz
struktura szablonów zostaną doprecyzowane na etapie implementacji, zgodnie z planem
działania z materiału Lekcji 28 (projektowanie modeli → migracje → panel admina → seeder →
widoki → testy). 