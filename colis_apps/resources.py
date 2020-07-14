from import_export import resources
from .models import Coli

class ColiResource(resources.ModelResource):

    class Meta:
        model = Coli
        exclude = ('id', )
        fields = ('dateheure','numero_colis', 'libelle','telephone_exp', 'nom_exp', 'telephone_dest', 'nom_dest','immatriculation__immatriculation', 'destination', 'valeur_declaree', 'montant')
        export_order = ('dateheure','numero_colis', 'libelle','telephone_exp', 'nom_exp', 'telephone_dest', 'nom_dest','immatriculation__immatriculation', 'destination', 'valeur_declaree', 'montant')