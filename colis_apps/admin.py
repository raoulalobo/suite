from django.contrib import admin
from .models import Coli, Profile, Client 
from import_export.admin import ImportExportModelAdmin
from .resources import ColiResource
# Register your models here.

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['id','client_created_at','phone','nom','cni','ville','quartier']
    list_filter = ['client_created_at', 'ville','quartier']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'date_of_birth']
    list_filter = ['phone', 'date_of_birth']


#@admin.register(Coli)
class ColiAdmin(ImportExportModelAdmin):
    resource_class = ColiResource
    list_display = ['dateheure', 'numero_colis', 'etat_colis', 'telephone_exp','telephone_dest', 'destination']
    list_filter = ['numero_colis', 'telephone_exp', 'telephone_dest']

admin.site.register(Coli, ColiAdmin)
