"""
Producent i konsument.
Klasyczny wzorzec współbieżności: producent dodaje elementy do bezpiecznej
wątkowo kolejki (queue.Queue), konsument je pobiera i przetwarza,
każdy w swoim własnym tempie.
"""
import threading
import queue
import time
import random

q = queue.Queue()
zakoncz = threading.Event()  # sygnał do zatrzymania obu wątków po czasie


def producent():
    """Co sekundę dodaje losową liczbę do kolejki."""
    while not zakoncz.is_set():
        element = random.randint(1, 100)
        q.put(element)
        print(f"[Producent] Dodano do kolejki: {element}")
        time.sleep(1)


def konsument():
    """Co 1.5 sekundy pobiera element z kolejki i go wypisuje."""
    while not zakoncz.is_set() or not q.empty():
        try:
            element = q.get(timeout=0.5)
            print(f"[Konsument] Pobrano z kolejki: {element}")
        except queue.Empty:
            continue
        time.sleep(1.5)


if __name__ == "__main__":
    watek_producent = threading.Thread(target=producent)
    watek_konsument = threading.Thread(target=konsument)

    watek_producent.start()
    watek_konsument.start()

    time.sleep(10)  # program działa przez 10 sekund
    zakoncz.set()

    watek_producent.join()
    watek_konsument.join()

    print("Program zakończony.") 