from django.db import models
import uuid 
from datetime import date

def f():
    d = uuid.uuid4()
    str = d.hex
    return str[0:16]

# Create your models here.
class Car(models.Model):
    id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False )
    immatriculation = models.CharField( max_length=100, default='N.A', unique=True  )
    seat = models.PositiveSmallIntegerField()
    chassis = models.CharField( max_length=100, default = 'N.A' )
    marque = models.CharField( max_length=100, default='N.A' )
    Type_vehicule = models.CharField( max_length=100, default='N.A' )
    annee_circulation = models.DateField( default=date.today )

    def __str__(self):
        return '{} ({})'.format( self.immatriculation , self.seat )

    class Meta:
        ordering = ["immatriculation"]

