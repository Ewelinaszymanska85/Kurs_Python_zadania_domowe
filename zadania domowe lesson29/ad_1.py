"""
Zadania w tle i skalowanie pracy z Celery w Django.

Polecenie: Zastanów się, w jaki sposób mógłbyś zintegrować Celery
ze swoją aplikacją. Czy widzisz korzyści ze zintegrowania jej ze
swoim projektem Django?

============================================================
KONTEKST
============================================================

Refleksja odnosi się do planowanego tematu pracy dyplomowej -
agregatora wiadomości (parsowanie artykułów z co najmniej dwóch
serwisów, publikacja treści przez użytkowników za zgodą admina).
To jeden z pięciu oficjalnych tematów do wyboru na Python Web
Development, rekomendowany przez nauczyciela właśnie w kontekście
wykorzystania feedparser + Celery + Redis.

============================================================
GDZIE CELERY PASOWAŁOBY NAJLEPIEJ
============================================================

1. Cykliczne pobieranie artykułów (Celery Beat)

   Agregator z założenia musi regularnie odpytywać zewnętrzne
   serwisy (kanały RSS) o nowe artykuły - np. co 15-30 minut.
   To dokładnie przypadek użycia Celery Beat pokazany w Bloku 4:
   Beat wysyła sygnał w zadanym interwale, a Worker wykonuje
   właściwe pobranie i przetworzenie danych.

   CELERY_BEAT_SCHEDULE = {
       'fetch-rss-feeds-every-30-min': {
           'task': 'news.tasks.fetch_all_feeds',
           'schedule': timedelta(minutes=30),
       },
   }

   Bez Celery, jedyną alternatywą byłby cron systemowy - ale
   materiał z lekcji jasno wskazuje, że cron nie pozwala na
   dynamiczne zlecanie zadań z poziomu kodu (np. natychmiastowe
   odświeżenie jednego, konkretnego źródła na żądanie admina).

2. Parsowanie i zapis artykułów jako osobne zadanie (task)

   Samo pobranie danych z feedparser oraz ich zapis do bazy
   (tworzenie obiektów Article, przypisanie kategorii/tagów)
   nie powinno blokować widoku HTTP. Zgodnie z zasadą z Bloku 3,
   do taska przekazywałabym wyłącznie identyfikator źródła
   (np. source_id), a nie cały obiekt Source - żeby uniknąć
   problemu z serializacją i nieaktualnymi danymi (stale data).

   @shared_task
   def fetch_feed_task(source_id):
       source = Source.objects.get(id=source_id)
       # parsowanie feedparser + tworzenie Article
       ...

3. Obsługa błędów i retry przy niestabilnych serwisach

   Zewnętrzne serwisy RSS bywają czasowo niedostępne (timeout,
   błąd 500, przeciążony serwer). Zamiast tracić całe zadanie
   przy jednym nieudanym połączeniu, zastosowałabym dokładnie
   wzorzec z Bloku 5 - bind=True + retry z countdown, tak żeby
   pojedynczy błąd sieciowy nie wymagał ręcznego ponawiania:

   @shared_task(bind=True, max_retries=3)
   def fetch_feed_task(self, source_id):
       try:
           ...
       except RequestException as exc:
           raise self.retry(exc=exc, countdown=60)

4. Idempotencja przy zapisie artykułów

   Ponieważ zadanie pobierania danego źródła może teoretycznie
   zostać wykonane dwukrotnie (np. przy restarcie brokera), zapis
   artykułów musi być idempotentny - czyli NIE dodawać duplikatu
   przy ponownym uruchomieniu tego samego zadania. W praktyce
   oznaczałoby to sprawdzanie unikalności po np. linku źródłowym
   artykułu (get_or_create zamiast bezwarunkowego create), zgodnie
   z zasadą z Bloku 5 ("dobra implementacja: transaction.status =
   PAID", a nie bezwarunkowe dodawanie).

5. Publikacja artykułów przez użytkowników za zgodą admina

   Jeśli w projekcie pojawi się dodatkowa funkcja przetwarzania
   treści zgłoszonych przez użytkowników (np. automatyczna
   moderacja, generowanie podsumowania artykułu), to również
   nadawałoby się na osobne zadanie w tle, zamiast blokować widok
   zapisu zgłoszenia na czas takiego przetwarzania.

============================================================
CZY WIDZĘ KORZYŚCI Z INTEGRACJI CELERY?
============================================================

Tak, i to w sposób, który wydaje mi się bardziej oczywisty niż
przy prostszych projektach z kursu (np. cacheproject). Agregator
wiadomości z definicji musi wykonywać powtarzalne, czasochłonne
operacje sieciowe (odpytywanie wielu zewnętrznych serwisów) w tle,
niezależnie od tego, czy w danym momencie ktokolwiek przegląda
stronę. To dokładnie scenariusz, w którym - zgodnie z materiałem
lekcji - zwykły widok Django (synchroniczny, blokujący worker)
zupełnie by się nie sprawdził: użytkownik odwiedzający stronę
główną nie powinien czekać, aż serwer w tym samym czasie odpyta
kilka zewnętrznych RSS-ów.

Największą korzyścią jest rozdzielenie w czasie momentu "pobrania
danych" od momentu "wyświetlenia danych użytkownikowi" - artykuły
są już zapisane w bazie, zanim ktokolwiek wejdzie na stronę, więc
sam request HTTP jest szybki i nie zależy od kondycji zewnętrznych
serwisów z wiadomościami.

Dodatkowym plusem jest to, że Celery Beat + Worker to naturalne
uzupełnienie tematów, które omawiałam wcześniej (cache w Lekcji 27
oraz drf-spectacular w Lekcji 28) - cały stos: Docker, Redis,
cache, dokumentacja API i teraz zadania w tle, składa się w spójny
obraz architektury zgodnej z wymaganiami na obronę pracy (Docker,
API, deployment).

============================================================
OGRANICZENIA, O KTÓRYCH TRZEBA PAMIĘTAĆ
============================================================

Zgodnie z sekcją "Limity Celery" - Celery nie jest bazą danych,
więc wynik przetwarzania (nowe artykuły) zawsze musi trafiać do
PostgreSQL/bazy danych, a nie być przechowywany tylko w wynikach
zadania. Poza tym warto pamiętać, że parsowanie RSS to operacja
głównie sieciowa (I/O), a nie "ciężkie obliczenia CPU" - więc
Celery jest tu odpowiednim narzędziem, w przeciwieństwie do np.
kodowania wideo, które i tak obciążyłoby workera w 100%.
"""