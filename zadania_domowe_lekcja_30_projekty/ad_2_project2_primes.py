"""
Projekt 2: Równoległy Generator Paczek Raportowych (CPU-bound)

============================================================
KOD ROZWIĄZANIA
============================================================
"""

from concurrent.futures import ProcessPoolExecutor
import math
import time
import multiprocessing


def is_prime(n: int) -> bool:
    """
    Klasyczna, nieoptymalna funkcja sprawdzająca, czy liczba jest
    pierwsza - sprawdza podzielność pętlą for od 2 do pierwiastka
    kwadratowego z n. Celowo nieoptymalna, żeby obciążyć CPU
    (zgodnie z wymaganiem zadania).
    """
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def process_range(bounds: tuple) -> list:
    """
    Przetwarza podany przedział liczb i zwraca listę wszystkich
    znalezionych w nim liczb pierwszych.
    """
    start, end = bounds
    return [n for n in range(start, end) if is_prime(n)]


if __name__ == "__main__":
    start_num = 1_000_000
    end_num = 1_300_000
    cpus = multiprocessing.cpu_count()

    # Podział zakresu na tyle fragmentów, ile jest rdzeni CPU
    chunk_size = (end_num - start_num) // cpus
    bounds_list = []
    for i in range(cpus):
        chunk_start = start_num + i * chunk_size
        # Ostatni fragment obejmuje resztę zakresu (na wypadek niepodzielności)
        chunk_end = end_num if i == cpus - 1 else chunk_start + chunk_size
        bounds_list.append((chunk_start, chunk_end))

    # --- Wersja równoległa (ProcessPoolExecutor) ---
    start_time = time.time()
    with ProcessPoolExecutor(max_workers=cpus) as executor:
        results = list(executor.map(process_range, bounds_list))

    # Złączenie wyników cząstkowych z wszystkich procesów w jedną listę
    all_primes = [prime for sublist in results for prime in sublist]
    parallel_time = time.time() - start_time

    print(f"Liczba rdzeni CPU: {cpus}")
    print(f"Znaleziono {len(all_primes)} liczb pierwszych w zakresie {start_num}-{end_num}")
    print(f"Czas wykonania równoległego: {parallel_time:.2f} s")

    # --- Wersja jednowątkowa (do porównania) ---
    start_time = time.time()
    single_thread_primes = process_range((start_num, end_num))
    single_time = time.time() - start_time

    print(f"Czas wykonania jednowątkowego: {single_time:.2f} s")
    print(f"Przyspieszenie: {single_time / parallel_time:.2f}x")


"""
============================================================
WYNIKI TESTU
============================================================

Liczba rdzeni CPU: 12
Znaleziono 21523 liczb pierwszych w zakresie 1000000-1300000
Czas wykonania równoległego: 1.06 s
Czas wykonania jednowątkowego: 2.40 s
Przyspieszenie: 2.27x

Wniosek

Wersja równoległa (ProcessPoolExecutor, 12 procesów) okazała się
ponad dwukrotnie szybsza od wersji jednowątkowej - to dobra
ilustracja tego, jak procesy pozwalają ominąć ograniczenie GIL
przy zadaniach CPU-bound (sprawdzanie podzielności liczb to czysto
obliczeniowa operacja procesora, bez żadnego oczekiwania na I/O).

Zwraca uwagę fakt, że przyspieszenie (2.27x) jest znacznie niższe
niż liczba dostępnych rdzeni (12x) - zjawisko to jest zgodne z
materiałem lekcji: każdy proces wymaga własnej, kosztownej
przestrzeni pamięci i własnej instancji interpretera Pythona, więc
narzut na utworzenie 12 procesów, podział danych między nie oraz
złączenie (i tak nierównomiernie rozłożonych, bo liczby pierwsze
nie występują równomiernie w każdym przedziale) wyników cząstkowych
"zjada" część teoretycznego zysku ze skalowania na wszystkie
rdzenie. Dodatkowo zakres 1 000 000 - 1 300 000 jest stosunkowo
niewielki, więc narzut na start procesów (który jest stały,
niezależnie od wielkości zadania) ma tu relatywnie większe
znaczenie niż przy dużo większym zbiorze danych.

Gdyby zamiast ProcessPoolExecutor użyto ThreadPoolExecutor (wątki)
do tego samego zadania, przyspieszenie praktycznie by nie
wystąpiło - GIL i tak pozwoliłby tylko jednemu wątkowi wykonywać
kod bajtowy Pythona w danym momencie, a dodatkowy narzut na
przełączanie kontekstu między wątkami mógłby nawet spowolnić
program względem wersji jednowątkowej. Wybór ProcessPoolExecutor
dla tego konkretnego, obliczeniowego zadania jest więc zgodny z
rekomendacją z tabeli podsumowującej w materiale lekcji
("Kompresja zdjęć, Generowanie PDF... -> ProcessPoolExecutor").
"""