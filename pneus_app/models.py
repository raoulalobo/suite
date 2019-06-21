import uuid
from django.db import models
from cars_app.models import Car 


# Create your models here.


class Pneu(models.Model):


    id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateTimeField()
    immatriculation = models.ForeignKey( Car, related_name='vehicule', on_delete=models.CASCADE)
    kilometrage = models.PositiveIntegerField()
    marque_pneu = models.CharField( max_length=50 )
    nbr_pneu = models.PositiveSmallIntegerField()
    responsable = models.CharField( max_length=50 )
    chauffeur = models.CharField( max_length=50 )
    observation = models.TextField()


    def __str__(self):
        return 'Changement de pneus, date : {} , immatriculation {} .'.format(self.date, self.immatriculation )

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "pneus"