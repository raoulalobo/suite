from django.contrib import admin
from .models import Pneu

# Register your models here.



@admin.register(Pneu)
class PlainteAdmin(admin.ModelAdmin):
    list_display = ['date', 'immatriculation', 'marque_pneu', 'nbr_pneu', 'observation']
    list_filter = ['immatriculation']
