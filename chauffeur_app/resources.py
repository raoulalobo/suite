from import_export import resources
from .models import Chauffeur

class ChauffeurResource(resources.ModelResource):

    class Meta:
        model = Chauffeur