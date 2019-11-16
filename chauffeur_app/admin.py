from django.contrib import admin
from .models import Personnel
from import_export.admin import ImportExportModelAdmin


# Register your models here.



@admin.register(Personnel)
class PersonnelAdmin(ImportExportModelAdmin):
    change_list_filter_template = "admin/filter_listing.html"
    list_display = ['nom', 'phone_1', 'phone_2']
    list_filter = ['nom']

