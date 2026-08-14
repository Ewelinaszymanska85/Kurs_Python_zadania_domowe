import asyncio


async def powitanie():
    """
    Korutyna - specjalna funkcja zdefiniowana przez 'async def'.
    Samo jej wywołanie (powitanie()) NIE uruchamia kodu w środku -
    tworzy tylko obiekt korutyny, gotowy do wykonania.
    """
    print("Gotowy do nauki!")


if __name__ == "__main__":
    # asyncio.run() tworzy pętlę zdarzeń, uruchamia w niej korutynę,
    # czeka na jej zakończenie, i bezpiecznie zamyka pętlę.
    asyncio.run(powitanie()) 
    
    
# Uruchom: python ad_1_pierwsza_korutyna.py 