from django.contrib import admin
from .models import Facture , Bleue , Bordereau , Categorie


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['categories']


@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ['date', 'libelle']


@admin.register(Bleue)
class BleueAdmin(admin.ModelAdmin):
    list_display = ['date', 'libelle']


@admin.register(Bordereau)
class BordereauAdmin(admin.ModelAdmin):
    list_display = ['date', 'libelle']

