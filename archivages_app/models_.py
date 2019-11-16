import uuid
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

    categories = models.CharField( max_length=50, default='N.A')

class ScanFacture(models.Model):

    file = models.FileField(null=True, blank=True )

    content_type =   models.ForeignKey(ContentType , on_delete=models.CASCADE )
    object_id = models.PositiveIntegerField()
    content_object=GenericForeignKey('content_type', 'object_id')
    #facture = models.ForeignKey( Scan , on_delete=models.CASCADE )


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
    dateheure = models.DateTimeField( auto_now=True )
    ville = models.CharField( max_length=16, choices=DESTINATION_CHOICES, default=NA, )
    cars = models.ForeignKey( Car, on_delete=models.CASCADE )
    observation = models.TextField()
    fichier = GenericRelation(ScanFacture)
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True


class Facture(Scan):

    #https://docs.djangoproject.com/fr/2.2/topics/i18n/timezones/
    categorie = models.ForeignKey( Categorie , on_delete=models.CASCADE )
    dateheurepaiement = models.DateField( default=timezone.now() ) 
    montant = models.PositiveIntegerField()
    libelle = models.CharField( max_length=50, default='N.A')
    demandeur = models.CharField( max_length=50, default='N.A')
    caissier = models.CharField( max_length=50, default='N.A')
    

class Bordereau(models.Model):


    date = models.DateTimeField( default=timezone.now() )
    ville = models.CharField( max_length=16, choices=DESTINATION_CHOICES, default=NA, )
    libelle = models.CharField( max_length=50, default='N.A')
    cars = models.ForeignKey( Car, on_delete=models.CASCADE )
    #A ajouter , mais sera note dans observation pour un debut
    #chauffeur = models.CharField( max_length=50, default='N.A')
    observation = models.TextField()
    history = HistoricalRecords()

    def __str__(self):
        return 'facture du {} .'.format(self.date )

    class Meta:
        ordering = ['-date',]


class ScanBordereau(models.Model):

    file = models.FileField(null=True, blank=True )
    bordereau = models.ForeignKey( Bordereau, on_delete=models.CASCADE )

    def __str__(self):
        return 'file {} '.format(self.bordereau)


class Bleue(models.Model):

    id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField( blank=True , null = True )
    numero = models.CharField( max_length=50, default='N.A', unique=True )
    cars = models.ForeignKey( Car, blank=True, null=True , on_delete=models.CASCADE )
    observation = models.TextField( blank=True, null=True )
    history = HistoricalRecords()

    def __str__(self):
        return 'numero carte bleue : #{} .'.format(self.numero )

    class Meta:
        ordering = ['-date',]


class ScanBleue(models.Model):

    file = models.FileField(null=True, blank=True )
    bleue = models.ForeignKey( Bleue, blank=True, null=True, on_delete=models.CASCADE )

    def __str__(self):
        return 'Scan carte grise #{} '.format(self.bleue)



class Assurance(models.Model):

    id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField( blank=True , null = True )
    numero = models.CharField( max_length=50, default='N.A', unique=True )
    cars = models.ForeignKey( Car, on_delete=models.CASCADE )
    observation = models.TextField()
    history = HistoricalRecords()

    def __str__(self):
        return 'numero carte bleue : #{} .'.format(self.numero )

    class Meta:
        ordering = ['-date',]


class ScanAssurance(models.Model):

    file = models.FileField(null=True, blank=True )
    bleue = models.ForeignKey( Bleue, on_delete=models.CASCADE )

    def __str__(self):
        return 'Scan carte grise #{} '.format(self.bleue)

