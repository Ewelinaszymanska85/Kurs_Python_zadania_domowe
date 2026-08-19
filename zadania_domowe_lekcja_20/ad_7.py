# ============================================================
# Zadanie 7 - Formularz dodawania produktu
# ============================================================


# ------------------------------------------------------------
# le20/forms.py
# (nowy plik)
# ------------------------------------------------------------
from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price']


# ------------------------------------------------------------
# le20/views.py
# (dopisać do istniejącego pliku - reszta widoków bez zmian)
# ------------------------------------------------------------
from django.shortcuts import render, redirect
from .forms import ProductForm


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product-list')
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})


# ------------------------------------------------------------
# Szablon: le20/pages/templates/add_product.html
# (osobny plik - patrz add_product.html)
# ------------------------------------------------------------


# ------------------------------------------------------------
# le20/le20/urls.py
# (PLIK GŁÓWNY PROJEKTU - to jest naprawa, nadpisz całą zawartość)
# ------------------------------------------------------------
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
]


# ------------------------------------------------------------
# le20/pages/urls.py
# (dopisać nową ścieżkę do listy urlpatterns - reszta bez zmian)
# ------------------------------------------------------------
from django.urls import path
from . import views

urlpatterns = [
    path('info/', views.info_view, name='info'),
    path('rules/', views.rules_view, name='rules'),
    path('user/<str:username>/', views.user_profile_view, name='user-profile'),
    path('products/', views.product_list_view, name='product-list'),
    path('notes/', views.note_list_view, name='note-list'),
    path('note/<int:note_id>/', views.note_detail_view, name='note-detail'),
    path('add_product/', views.add_product, name='add_product'),
] 