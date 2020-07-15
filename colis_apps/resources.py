from import_export import resources
from .models import Coli

class ColiResource(resources.ModelResource):

    class Meta:
        model = Coli