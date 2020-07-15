from django.contrib import admin
from .models import Coli, Profile, Client , Retour
from import_export.admin import ImportExportModelAdmin
# Register your models here.

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['created', 'last_transaction', 'phone','nom','ville','quartier']
    list_filter = ['created', 'ville','quartier']


@admin.register(Retour)
class RetourAdmin(admin.ModelAdmin):
    list_display = ['created', 'last_transaction', 'phone','role','appele','satisfait']
    list_filter = ['created','phone', 'appele','satisfait']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'date_of_birth']
    list_filter = ['phone', 'date_of_birth']


@admin.register(Coli)
class ColiAdmin(ImportExportModelAdmin):
    change_list_filter_template = "admin/filter_listing.html"
    list_display = ['dateheure', 'numero_colis', 'nom_exp' , 'telephone_exp', 'nom_dest' , 'telephone_dest', 'destination' ,'valeur_declaree', 'montant' , 'libelle' , 'immatriculation', 'etat_colis']
    list_filter = ['numero_colis', 'telephone_exp', 'telephone_dest']
