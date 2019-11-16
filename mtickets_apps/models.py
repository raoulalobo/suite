import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from simple_history.models import HistoricalRecords
from django.core.validators import MaxValueValidator


class Partner(models.Model):
    id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False )
    nom = models.CharField( max_length=100, default='N.A' )
    telephones = models.CharField( max_length=100, default='N.A' )
    plateforme = models.CharField( max_length=100, default='N.A')
    passw = models.CharField( max_length=100, default='N.A' )
    observation = models.TextField()
    history = HistoricalRecords()

    def __str__(self):
        return self.nom

    class Meta:
        ordering = ["nom"]
        

class Mticket(models.Model):

    YAOUNDE = 'YDE'
    DOUALA = 'DLA'
    NA = 'NA'
    DESTINATION_CHOICES = (
        (YAOUNDE, 'Yaounde'),
        (DOUALA, 'Douala'),
        (NA, 'NA'),
    )
    id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False)
    #addtime = l'heure d'ajout enregistre par la machine
    dateheure = models.DateTimeField( auto_now=True )
    ticket = models.CharField( max_length=100, default='N.A' , unique=True )
    cni = models.CharField( max_length=100, default='N.A' )
    name = models.CharField( max_length=100, default='N.A' )
    #destination = models.CharField( max_length=16, choices=DESTINATION_CHOICES, default=NA, )
    partner = models.ForeignKey( Partner, related_name='partenaire', on_delete=models.CASCADE)
    observation = models.TextField()
    history = HistoricalRecords()

    def __str__(self):
        return 'mticket #{} , partenaire {} .'.format(self.ticket, self.partner )

    class Meta:
        ordering = ['-dateheure','ticket']


