"""
Projekt 1: Wielowątkowy Downloader Plików z Licznikiem Postępu

============================================================
KOD ROZWIĄZANIA
============================================================
"""

import concurrent.futures
import requests
import threading
import time

total_bytes_downloaded = 0
bytes_lock = threading.Lock()

# UWAGA: pierwotnie użyto https://httpbin.org, jednak serwis okazał się
# niedostępny (błąd 503 Service Temporarily Unavailable) - problem
# potwierdzony jako znany, powtarzający się problem tego darmowego
# serwisu, niezwiązany z konfiguracją sieci czy kodem. Zastąpiono
# adresem httpbingo.org - kompatybilnym, aktywnie utrzymywanym
# fork'iem oferującym te same endpointy (w tym /bytes/:n).
URLS = [f"https://httpbingo.org/bytes/{size}" for size in [500, 1200, 3500, 800, 2400]]


def download_url(url: str, retries: int = 3):
    """
    Pobiera zawartość z podanego URL, mierzy rozmiar odpowiedzi
    w bajtach i bezpiecznie (przy pomocy Lock) aktualizuje globalny
    licznik total_bytes_downloaded, współdzielony przez wiele wątków.

    Dodatkowo zawiera prosty mechanizm ponawiania (retry), na wypadek
    chwilowej niedostępności serwera testowego.
    """
    global total_bytes_downloaded

    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            size = len(response.content)

            # Sekcja krytyczna - tylko jeden wątek na raz może
            # modyfikować total_bytes_downloaded
            with bytes_lock:
                total_bytes_downloaded += size

            print(f"[{threading.current_thread().name}] Pobrano {size} bajtów z {url}")
            return size

        except requests.RequestException as exc:
            print(f"[{threading.current_thread().name}] Próba {attempt + 1}/{retries} nieudana dla {url}: {exc}")
            time.sleep(2)

    print(f"[{threading.current_thread().name}] Ostatecznie nie udało się pobrać {url}")
    return 0


if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(download_url, url): url for url in URLS}

        for future in concurrent.futures.as_completed(futures):
            url = futures[future]
            try:
                future.result()
            except Exception as exc:
                print(f"Wyjątek dla {url}: {exc}")

    print(f"\n=== RAPORT KOŃCOWY ===")
    print(f"Łącznie pobrano: {total_bytes_downloaded} bajtów")


"""
============================================================
WYNIKI TESTU
============================================================

[ThreadPoolExecutor-0_0] Pobrano 500 bajtów z https://httpbingo.org/bytes/500
[ThreadPoolExecutor-0_2] Pobrano 3500 bajtów z https://httpbingo.org/bytes/3500
[ThreadPoolExecutor-0_1] Pobrano 1200 bajtów z https://httpbingo.org/bytes/1200
[ThreadPoolExecutor-0_2] Pobrano 2400 bajtów z https://httpbingo.org/bytes/2400
[ThreadPoolExecutor-0_0] Pobrano 800 bajtów z https://httpbingo.org/bytes/800

=== RAPORT KOŃCOWY ===
Łącznie pobrano: 8400 bajtów

Suma zgadza się matematycznie: 500 + 3500 + 1200 + 2400 + 800 = 8400.

Napotkana trudność

Pierwotny adres testowy (httpbin.org) okazał się notorycznie
niedostępny (błąd 503), co jest udokumentowanym, powtarzającym
się problemem tego darmowego serwisu, niezależnym od konfiguracji
projektu. Rozwiązaniem było przełączenie się na httpbingo.org -
kompatybilny fork oferujący identyczne endpointy. Dodatkowo dodano
prosty mechanizm retry (3 próby z 2-sekundowym odstępem) dla
większej odporności na chwilowe problemy sieciowe.

Wniosek

Wynik potwierdza poprawne działanie mechanizmu ThreadPoolExecutor
przy zadaniach I/O-bound (zapytania HTTP). Widać w logach, że
pojedynczy wątek z puli (np. ThreadPoolExecutor-0_0) obsłużył
więcej niż jedno zadanie po kolei - to dokładnie ilustruje
"reużywalność wątków" opisaną w materiale (pula tworzy określoną
liczbę wątków i używa ich wielokrotnie, zamiast tworzyć nowy wątek
dla każdego zadania). Globalny licznik total_bytes_downloaded
został poprawnie zaktualizowany przez wszystkie wątki bez utraty
danych, dzięki zastosowaniu threading.Lock w sekcji krytycznej -
bez tego zabezpieczenia wynik końcowy mógłby być niższy niż
rzeczywista suma pobranych bajtów (klasyczny problem Race
Condition opisany w materiale lekcji).
"""