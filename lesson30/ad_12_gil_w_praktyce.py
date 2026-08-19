"""
GIL w praktyce (CPU-bound).
Porównuje czas wykonania intensywnych obliczeń: sekwencyjnie, w dwóch
wątkach jednocześnie, i w dwóch procesach jednocześnie - pokazuje
realny wpływ Global Interpreter Lock na zadania obciążające CPU.
"""
import threading
import multiprocessing
import time


def oblicz():
    """Intensywne obliczenia CPU-bound."""
    return sum(i * i for i in range(20_000_000))


if __name__ == "__main__":
    # --- Sekwencyjnie (dwa razy pod rząd) ---
    start = time.time()
    oblicz()
    oblicz()
    czas_sekwencyjny = time.time() - start
    print(f"Czas sekwencyjny (2x): {czas_sekwencyjny:.2f}s")

    # --- Dwa wątki jednocześnie ---
    start = time.time()
    w1 = threading.Thread(target=oblicz)
    w2 = threading.Thread(target=oblicz)
    w1.start()
    w2.start()
    w1.join()
    w2.join()
    czas_watki = time.time() - start
    print(f"Czas z 2 wątkami: {czas_watki:.2f}s")

    # --- Dwa procesy jednocześnie ---
    start = time.time()
    p1 = multiprocessing.Process(target=oblicz)
    p2 = multiprocessing.Process(target=oblicz)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    czas_procesy = time.time() - start
    print(f"Czas z 2 procesami: {czas_procesy:.2f}s")

    print("\n--- WNIOSEK ---")
    print(f"Wątki NIE przyspieszają obliczeń CPU-bound (czas ~{czas_watki:.2f}s")
    print(f"jest zbliżony do 2x czas sekwencyjny), ponieważ GIL pozwala")
    print(f"tylko jednemu wątkowi na raz wykonywać kod bajtowy Pythona -")
    print(f"wątki NIE dają prawdziwej równoległości dla zadań CPU-bound.")
    print(f"Procesy (czas ~{czas_procesy:.2f}s, bliższy czasowi pojedynczego")
    print(f"wywołania) omijają GIL, bo każdy proces ma WŁASNY interpreter")
    print(f"Pythona i własną pamięć - to daje prawdziwą równoległość.")