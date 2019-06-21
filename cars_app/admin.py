from django.contrib import admin
from .models import Car , CarteBleue, CarteGrise
from import_export.admin import ImportExportModelAdmin


# Register your models here.



@admin.register(Car)
class CarAdmin(ImportExportModelAdmin):
    change_list_filter_template = "admin/filter_listing.html"
    #change_list_template = "admin/change_list_filter_sidebar.html"
    list_display = ['immatriculation', 'seat']
    list_filter = ['immatriculation', 'seat']


@admin.register(CarteBleue)
class CarteBleueAdmin(ImportExportModelAdmin):
    #change_list_template = "admin/change_list_filter_sidebar.html"
    list_display = ['numero', 'validite', 'immatriculation']
    list_filter = ['immatriculation']

@admin.register(CarteGrise)
class CarteGriseAdmin(ImportExportModelAdmin):
    list_display = ['numero', 'validite', 'immatriculation']
    list_filter = ['immatriculation']
