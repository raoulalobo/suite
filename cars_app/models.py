from django.db import models
import uuid 

# Create your models here.

class Car(models.Model):
    id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False )
    immatriculation = models.CharField( max_length=100, default='N.A' )
    seat = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.immatriculation

    class Meta:
        ordering = ["immatriculation"]


class CarteGrise(models.Model):
    id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False )
    numero = models.CharField(max_length=100, null=True )
    immatriculation = models.ForeignKey( Car, on_delete=models.CASCADE )
    validite = models.DateTimeField()

    def _str_(self):
        return 'Numero : {}'.format(self.numero)


class CarteBleue(models.Model):
    id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False )
    numero = models.CharField(max_length=100, null=True )
    immatriculation = models.ForeignKey( Car, on_delete=models.CASCADE )
    validite = models.DateTimeField()

    def _str_(self):
        return 'Numero : {}'.format(self.numero)