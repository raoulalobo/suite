import uuid
from datetime import date
from django.utils import timezone
from django.db import models
from cars_app.models import Car
from django.conf import settings 
from django.utils import timezone
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from simple_history.models import HistoricalRecords
from django.core.validators import MaxValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation



class Categorie(models.Model):

    categories = models.CharField( max_length=50, default='N.A', unique=True )

    def __str__(self):
        return self.categories


class Scan(models.Model):

    YAOUNDE = 'YDE'
    DOUALA = 'DLA'
    NA = 'NA'
    DESTINATION_CHOICES = (
        (YAOUNDE, 'Yaounde'),
        (DOUALA, 'Douala'),
        (NA, 'NA'),
    )
    id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False)
    dateheure_saisie = models.DateTimeField( auto_now=True )
    date = models.DateField( default=date.today )
    libelle = models.CharField( max_length=500, default='N.A')
    ville = models.CharField( max_length=16, choices=DESTINATION_CHOICES, default=NA, )
    cars = models.ForeignKey( Car, on_delete=models.CASCADE )
    observation = models.TextField()
    history = HistoricalRecords(inherit=True)

    def __str__(self):
        return '{}'.format( self.libelle )

    class Meta:
        ordering = ['-date']


class ScanFichier(models.Model):

    file = models.FileField(null=True, blank=True )
    scanfichier = models.ForeignKey( Scan , on_delete=models.CASCADE )

class Roue(Scan):

    kilometrage = models.PositiveIntegerField()
    marque_pneu = models.CharField( max_length=50 )
    nbr_pneu = models.PositiveSmallIntegerField()
    responsable = models.CharField( max_length=50 )
    chauffeur = models.CharField( max_length=50 )



class Facture(Scan):
 
    categorie = models.ForeignKey( Categorie , on_delete=models.CASCADE , default=1 )
    montant = models.PositiveIntegerField()
    demandeur = models.CharField( max_length=50, default='N.A')
    caissier = models.CharField( max_length=50, default='N.A')
    

class Bordereau(Scan):

    pass

    #date = models.DateTimeField( default=timezone.now )
    #A ajouter , mais sera note dans observation pour un debut
    #chauffeur = models.CharField( max_length=50, default='N.A')

class Bleue(Scan):

    numero_bleue = models.CharField( max_length=50, unique=True, default='N.A'  )

class Assurance(Scan):

    numero_assurance = models.CharField( max_length=50,  unique=True, default='N.A' )

class Plainte(Scan):
    OUI = 'OUI'
    NON = 'NON'
    NA = 'NA'
    STATUS_CHOICES = (
        (OUI, 'Oui'),
        (NON, 'Non'),
        (NA, 'NA'),
    )
    plaignant = models.CharField( max_length=50, default='N.A' )
    phone = models.CharField( max_length=50, default='N.A' )
    status = models.CharField( max_length=16, choices=STATUS_CHOICES, default=NA, )


class Explication(Scan):
    OUI = 'OUI'
    NON = 'NON'

    STATUS_CHOICES = (
        (OUI, 'OUI'),
        (NON, 'NON'),
    )
    nom = models.CharField( max_length=50, default='N.A' )
    poste = models.CharField( max_length=50, default='N.A' )
    #Scan._meta.get_field('cars').max_length = 255
    reponse = models.CharField( max_length=16, choices=STATUS_CHOICES, default=NON, )



