from django.contrib import admin
from .models import Car 
from import_export.admin import ImportExportModelAdmin


# Register your models here.



@admin.register(Car)
class CarAdmin(ImportExportModelAdmin):
    change_list_filter_template = "admin/filter_listing.html"
    #change_list_template = "admin/change_list_filter_sidebar.html"
    list_display = ['immatriculation', 'seat']
    list_filter = ['immatriculation', 'seat']
