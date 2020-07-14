import uuid
from django.db import models
from cars_app.models import Car 
from django.utils import timezone
from simple_history.models import HistoricalRecords
from django.core.validators import MaxValueValidator

from django.conf import settings
from django.contrib.auth.models import User


class Voyage(models.Model):

    YAOUNDE = 'YDE'
    DOUALA = 'DLA'
    NA = 'NA'
    DESTINATION_CHOICES = (
        (YAOUNDE, 'Yaounde'),
        (DOUALA, 'Douala'),
        (NA, 'NA'),
    )
    id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False)
    date_added = models.DateTimeField( auto_now_add=True )
    last_modification = models.DateTimeField( auto_now=True )
    chauffeur = models.CharField( max_length=100 , blank=True )
    bagagiste = models.CharField( max_length=100 , blank=True )
    destination = models.CharField( max_length=16, choices=DESTINATION_CHOICES, default=NA, )
    immatriculation = models.ForeignKey( Car, related_name='car', on_delete=models.SET_NULL)
    complete = models.BooleanField( default=False )
    observation = models.TextField(blank=True)
    history = HistoricalRecords()


    def __str__(self):
        return 'voyage {} '.format(self.date_added)

    class Meta:
        ordering = ['-date_added']



class Bagage(models.Model):

    id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False)
    date_added = models.DateTimeField( auto_now_add=True )
    last_modification = models.DateTimeField( auto_now=True )
    owner_name = models.CharField( max_length=100 , blank=True )
    owner_address = models.CharField( max_length=100 , blank=True )
    seat = models.CharField( max_length=100 , blank=True )
    quantity = models.IntegerField( default=0 , blank=True, null=True )
    image = models.ImageField(upload_to='products/%Y/%m/%d',blank=True)
    observation = models.TextField(blank=True)
    history = HistoricalRecords()


    def __str__(self):
        return 'bagage {} '.format(self.date_added)

    class Meta:
        ordering = ['-date_added']



class BagageDeVoyage(models.Model):

    id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False)
    date_added = models.DateTimeField( auto_now_add=True )
    voyage = models.ForeignKey( Voyage, related_name='trip', on_delete=models.SET_NULL , blank=True, null=True)
    bagage = models.ForeignKey( Bagage, related_name='bagage', on_delete=models.SET_NULL, blank=True, null=True)




