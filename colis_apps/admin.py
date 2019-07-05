from django.contrib import admin
from .models import Coli, Profile

# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'date_of_birth']
    list_filter = ['phone', 'date_of_birth']


@admin.register(Coli)
class PlainteAdmin(admin.ModelAdmin):
    list_display = ['dateheure', 'numero_colis', 'etat_colis', 'telephone_exp', 'telephone_dest', 'destination']
    list_filter = ['numero_colis', 'telephone_exp', 'telephone_dest']

#admin.site.register( DataBase )