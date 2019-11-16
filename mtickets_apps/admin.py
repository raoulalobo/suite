from django.contrib import admin
from .models import Partner, Mticket

# Register your models here.

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['nom','plateforme','passw']
    list_filter = ['nom']


@admin.register(Mticket)
class MticketAdmin(admin.ModelAdmin):
    list_display = ['dateheure', 'ticket', 'cni']
    list_filter = ['partner']

#admin.site.register( DataBase )