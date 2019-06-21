
from django.db import models
import uuid

# Create your models here.

class Plainte(models.Model):

    REMBOURSEMENT = 'Remboursement'
    COLIS = 'Colis'
    BAGAGES = 'Bagages'
    AUTRES = 'Autres'
    RAISON_CHOICES = (
        (REMBOURSEMENT, 'Remboursement'),
        (COLIS, 'Colis'),
        (BAGAGES, 'Bagages'),
        (AUTRES, 'Autres'),
    )

    YAOUNDE = 'YDE'
    DOUALA = 'DLA'
    NOTAVAILABLE = 'N.A'
    DESTINATION_CHOICES = (
        (YAOUNDE, 'Yaounde'),
        (DOUALA, 'Douala'),
        (NOTAVAILABLE, 'not available'),
    )

    TRAITE = 'traite'
    NON_TRAITE = 'non traite'
    ETAT_CHOICES = (
        (TRAITE, 'traite'),
        (NON_TRAITE, 'non traite'),
    )

    id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False)
    dateheure = models.DateTimeField()
    ville_plainte = models.CharField(
        max_length=16,
        choices=DESTINATION_CHOICES,
        default=NOTAVAILABLE,
    )
    raison_plainte = models.CharField(
        max_length=16,
        choices=RAISON_CHOICES,
        default=COLIS,
    )
    etat_plainte = models.CharField(
        max_length=10,
        choices=ETAT_CHOICES,
        default=NON_TRAITE,
    )
    libelle = models.CharField( max_length=100, default='N.A')
    plaignant = models.CharField( max_length=100, default='N.A')
    telephone_p = models.CharField( max_length=100, default='N.A' )
    detail_plainte = models.TextField()
    #image_plainte = models.ImageField(upload_to='img/%Y/%m/%d/')
    numero_colis = models.CharField( max_length=100, default='N.A' )
    immatriculation = models.CharField( max_length=100, default='N.A' )
    resolution_observation = models.TextField()

    def __str__(self):
        return 'Plainte du {} , {} a {}'.format(self.dateheure, self.raison_plainte, self.ville_plainte)


class PlainteFile(models.Model):

    file = models.FileField( upload_to="files/%Y/%m/%d" )
    plainte = models.ForeignKey( Plainte, on_delete=models.CASCADE )

    def __str__(self):
        return 'file {} '.format(self.plainte)
