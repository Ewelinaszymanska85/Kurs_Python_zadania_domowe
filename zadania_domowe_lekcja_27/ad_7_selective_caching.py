"""
Zadanie domowe 7 - Cache w Django REST Framework
Selektywne cachowanie w widoku - niskopoziomowe API cache.

Kompletne rozwiązanie zadania obejmuje widok łączący dwa źródła
danych: proste zapytanie do bazy (niecachowane) oraz symulację
kosztownych obliczeń (cachowaną osobno przy pomocy cache.get/cache.set).

============================================================
WIDOK (products/views.py) - fragment z nowymi elementami
============================================================
"""

import time
from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer


def get_complex_calculation_result():
    """
    Symuluje kosztowną, długotrwałą operację, buforując jej wynik
    na 60 sekund przy pomocy niskopoziomowego API cache.

    Dzięki temu tylko WYNIK OBLICZEŃ jest buforowany - a nie cała
    odpowiedź HTTP widoku, jak przy @cache_page.
    """
    cache_key = 'complex_calculation_result'
    result = cache.get(cache_key)

    if result is None:
        time.sleep(3)
        result = {
            "calculation": "suma_cen_wszystkich_produktow",
            "value": float(sum(p.price for p in Product.objects.all())),
            "source": "obliczone na żywo",
        }
        cache.set(cache_key, result, timeout=60)
    else:
        result = dict(result)
        result["source"] = "pobrane z cache"

    return result


@api_view(['GET'])
def product_summary_view(request):
    """
    Widok łączący proste zapytanie do bazy (produkty - zawsze
    świeże) z buforowanym wynikiem kosztownych obliczeń.
    """
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)

    calculation_result = get_complex_calculation_result()

    return Response({
        "products": serializer.data,
        "calculation_result": calculation_result,
    })


"""
============================================================
ŚCIEŻKA URL (cacheproject/urls.py) - fragment do dodania:
============================================================

path('api/product-summary/', views.product_summary_view, name='product_summary'),

============================================================
WYNIKI TESTÓW W POSTMANIE
============================================================

Test 1: GET /api/product-summary/ (zaraz po cache.clear())
Czas odpowiedzi: 3.48 s
"source": "obliczone na żywo"

Test 2: GET /api/product-summary/ (natychmiast po Teście 1)
Czas odpowiedzi: 43 ms
"source": "pobrane z cache"

Wniosek

Niskopoziomowe API cache (cache.get/cache.set) pozwala na
precyzyjną kontrolę nad tym, CO dokładnie jest buforowane -
w tym przypadku tylko wynik kosztownych obliczeń (symulowanych
przez time.sleep(3)), podczas gdy proste zapytanie do bazy danych
(lista produktów) wykonuje się przy każdym żądaniu na nowo,
zapewniając zawsze aktualne dane. To bardziej precyzyjne podejście
niż @cache_page, które buforuje CAŁĄ odpowiedź widoku.
"""