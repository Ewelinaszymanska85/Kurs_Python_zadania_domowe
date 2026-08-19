"""
Prosty web crawler.
Pobiera strony z jednej domeny i wyszukuje kolejne linki.
Do współbieżnego pobierania stron wykorzystuje pulę wątków.
"""
import threading
import queue
import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


START_URL = "https://example.com"
MAX_STRON = 50
LICZBA_WATKOW = 5

kolejka = queue.Queue()
odwiedzone = set()
blokada = threading.Lock()


def pobierz_strone(url):
    """Pobiera zawartość strony."""

    try:
        odpowiedz = requests.get(
            url,
            timeout=5,
            headers={"User-Agent": "PythonCrawler/1.0"}
        )
        odpowiedz.raise_for_status()
        return odpowiedz.text

    except requests.RequestException as blad:
        print(f"Błąd pobierania {url}: {blad}")
        return None


def znajdz_linki(html, url, domena):
    """Zwraca linki należące do tej samej domeny."""

    soup = BeautifulSoup(html, "html.parser")
    linki = []

    for element in soup.find_all("a", href=True):
        link = urljoin(url, element["href"])
        dane = urlparse(link)

        if dane.netloc == domena:
            linki.append(link)

    return linki


def worker(domena):
    """Pobiera strony i dodaje znalezione linki do kolejki."""

    while True:
        try:
            url = kolejka.get(timeout=2)
        except queue.Empty:
            return

        try:
            print(f"Pobieram: {url}")

            html = pobierz_strone(url)

            if html:
                for link in znajdz_linki(html, url, domena):

                    with blokada:
                        if (
                            link not in odwiedzone
                            and len(odwiedzone) < MAX_STRON
                        ):
                            odwiedzone.add(link)
                            kolejka.put(link)

        finally:
            kolejka.task_done()


if __name__ == "__main__":
    domena = urlparse(START_URL).netloc

    odwiedzone.add(START_URL)
    kolejka.put(START_URL)

    watki = []

    for _ in range(LICZBA_WATKOW):
        watek = threading.Thread(
            target=worker,
            args=(domena,)
        )
        watki.append(watek)
        watek.start()

    kolejka.join()

    for watek in watki:
        watek.join()

    print("\n=== CRAWLER ZAKOŃCZONY ===")
    print(f"Odwiedzono stron: {len(odwiedzone)}")

    for url in odwiedzone:
        print(url)