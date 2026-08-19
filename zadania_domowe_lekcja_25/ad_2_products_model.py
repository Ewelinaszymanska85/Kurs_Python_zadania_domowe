"""
Zadanie domowe 2 - Wprowadzenie do Django REST Framework
Prosty model i serializator - Product.

Kompletne rozwiązanie zadania obejmuje dwa elementy:
1. Model Product (poniżej, aktywny kod)
2. Serializator ProductSerializer (dołączony jako komentarz referencyjny)

============================================================
1. MODEL (products/models.py)
============================================================
"""

from django.db import models


class Product(models.Model):
    """
    Model reprezentujący pojedynczy produkt. 

    Pola:
        name (str): Nazwa produktu.
        price (Decimal): Cena produktu.
    """

    name = models.CharField(
        max_length=200,
        verbose_name="Nazwa"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Cena"
    )

    def __str__(self):
        return self.name


"""
============================================================
2. SERIALIZATOR (products/serializers.py) - pełna zawartość:
============================================================

from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'price']
""" 