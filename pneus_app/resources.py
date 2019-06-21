from import_export import resources
from import_export.fields import Field
from .models import Pneu

#Pour export-import cvs , excel

class PneuResource(resources.ModelResource):
    date = Field(attribute='date', column_name='Date')
    immatriculation = Field(attribute='immatriculation__immatriculation', column_name='Imm.')
    marque_pneu = Field(attribute='marque_pneu', column_name='Marque')

    class Meta:
        model = Pneu
        fields = ( 'date', 'immatriculation', 'kilometrage', 'marque_pneu', 'nbr_pneu', 'chauffeur')