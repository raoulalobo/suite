#en dessous pour l'import export du cote admin
#from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Plainte

# Register your models here.



@admin.register(Plainte)
class PlainteAdmin(admin.ModelAdmin):
    list_display = ['dateheure', 'raison_plainte', 'plaignant', 'resolution_observation']
    list_filter = ['raison_plainte']

#admin.site.register( DataBase )

