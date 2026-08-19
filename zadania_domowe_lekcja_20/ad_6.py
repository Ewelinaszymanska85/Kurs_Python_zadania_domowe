# =============================================================================
# ZADANIE 6: Aplikacja "Notatnik" (challenge)
# =============================================================================


# -----------------------------------------------------------------------------
# pages/models.py  (fragment - dodany model Note)
# -----------------------------------------------------------------------------
from django.db import models


class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title


# Komendy wykonane po zdefiniowaniu modelu:
#
#     python manage.py makemigrations
#     python manage.py migrate
#
# Efekt:
#     Migrations for 'pages':
#       pages\migrations\0002_note.py
#         + Create model Note
#     Applying pages.0002_note... OK


# Komendy wykonane w manage.py shell (dodanie danych testowych):
#
#     python manage.py shell
#
#     from pages.models import Note
#     Note.objects.create(title="Lista zakupów", content="Mleko, chleb, jajka, masło")
#     Note.objects.create(title="Plan na weekend", content="Posprzątać dom, ugotować obiad, obejrzeć film")
#     exit()


# -----------------------------------------------------------------------------
# pages/views.py  (fragment - dodane widoki note_list_view i note_detail_view)
# -----------------------------------------------------------------------------
from django.shortcuts import render
from .models import Note


def note_list_view(request):
    """Widok wyświetlający listę wszystkich notatek."""
    notes = Note.objects.all()
    return render(request, "pages/note_list.html", {"notes": notes})


def note_detail_view(request, note_id):
    """Widok wyświetlający szczegóły jednej notatki."""
    note = Note.objects.get(id=note_id)
    return render(request, "pages/note_detail.html", {"note": note})


# -----------------------------------------------------------------------------
# pages/urls.py  (fragment - dodane trasy notes/ i note/<note_id>/)
# -----------------------------------------------------------------------------
urlpatterns_fragment = """
path('notes/', views.note_list_view, name='note-list'),
path('note/<int:note_id>/', views.note_detail_view, name='note-detail'),
"""


# -----------------------------------------------------------------------------
# pages/templates/pages/note_list.html
# -----------------------------------------------------------------------------
note_list_html = """
{% extends "base.html" %}

{% block title %}Lista notatek{% endblock %}

{% block content %}
<h2>Notatki</h2>
<ul>
    {% for note in notes %}
    <li><a href="/note/{{ note.id }}/">{{ note.title }}</a></li>
    {% endfor %}
</ul>
{% endblock %}
"""


# -----------------------------------------------------------------------------
# pages/templates/pages/note_detail.html
# -----------------------------------------------------------------------------
note_detail_html = """
{% extends "base.html" %}

{% block title %}{{ note.title }}{% endblock %}

{% block content %}
<h2>{{ note.title }}</h2>
<p>{{ note.content }}</p>
{% endblock %}
""" 