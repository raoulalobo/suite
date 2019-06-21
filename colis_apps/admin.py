from django.contrib import admin
from .models import Coli

# Register your models here.



@admin.register(Coli)
class PlainteAdmin(admin.ModelAdmin):
    list_display = ['dateheure', 'numero_colis', 'etat_colis', 'telephone_exp', 'telephone_dest', 'destination']
    list_filter = ['numero_colis', 'telephone_exp', 'telephone_dest']

#admin.site.register( DataBase )