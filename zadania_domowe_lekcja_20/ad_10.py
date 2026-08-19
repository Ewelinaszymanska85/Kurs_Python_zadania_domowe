# ============================================================
# Zadanie 10 - Dodaj paginację do listy notatek
# ============================================================


# ------------------------------------------------------------
# le20/pages/views.py
# (dopisać import na górze pliku + zamienić istniejącą funkcję
#  note_list_view na poniższą wersję - reszta widoków bez zmian)
# ------------------------------------------------------------
from django.core.paginator import Paginator


def note_list_view(request):
    """Widok wyświetlający listę wszystkich notatek, z paginacją (3 na stronę)."""
    all_notes = Note.objects.all()
    paginator = Paginator(all_notes, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "pages/note_list.html", {"page_obj": page_obj}) 