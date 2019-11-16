from django.utils import timezone
from django.db import models
import uuid 


# Create your models here.

class Personnel(models.Model):
        
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    NA = 'NA'
    GENRE_CHOICES = (
        (MALE, 'Yaounde'),
        (FEMALE, 'FEMALE'),
        (NA, 'NA'),
    )
    id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False )
    nom = models.CharField( max_length=100, default='N.A' )
    phone_1 = models.CharField( max_length=100, default='N.A' )
    phone_2 = models.CharField( max_length=100, default='N.A' )
    birthday = models.DateField( null=True, blank=True )
    genre = models.CharField( max_length=16, choices=GENRE_CHOICES, default=NA, )

    def __str__(self):
        return self.nom

    class Meta:
        ordering = ["nom"]
