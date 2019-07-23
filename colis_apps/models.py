import uuid
from django.db import models
from cars_app.models import Car 
from django.utils import timezone
from simple_history.models import HistoricalRecords
from django.core.validators import MaxValueValidator

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Signal
class Profile(models.Model):

    #user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    user = models.OneToOneField( User ,on_delete=models.CASCADE)
    phone = models.CharField(max_length=30, default='697509899' )
    date_of_birth = models.DateField(blank=True, null=True)
    #photo = models.ImageField(upload_to='users/%Y/%m/%d/',blank=True,null=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# A  comprendre .
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    profile = Profile.objects.get_or_create(user=instance)
    instance.profile.save()
    #if instance.profile :
    #    instance.profile.save()
    #else :
    #    Profile.objects.create(user=instance)

# Create your models here.

class ColiManager(models.Manager):
    def yde(self):
        return self.filter(destination='YDE')

    def dla(self, size):
        return self.filter(destination='DLA')
        

class Coli(models.Model):

    YAOUNDE = 'YDE'
    DOUALA = 'DLA'
    NA = 'NA'
    DESTINATION_CHOICES = (
        (YAOUNDE, 'Yaounde'),
        (DOUALA, 'Douala'),
        (NA, 'NA'),
    )
    ENVOYE = 'envoye'
    RECU = 'recu'
    RETIRE = 'retire'
    ETAT_CHOICES = (
        (ENVOYE, 'envoye'),
        (RECU, 'recu'),
        (RETIRE, 'retire'),
    )
    id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False)
    #addtime = l'heure d'ajout enregistre par la machine
    dateheure = models.DateTimeField( auto_now=True )
    numero_colis = models.CharField( max_length=100, default='N.A' , unique=True )
    telephone_exp = models.CharField( max_length=100, default='N.A' )
    telephone_dest = models.CharField( max_length=100, default='N.A' )
    destination = models.CharField( max_length=16, choices=DESTINATION_CHOICES, default=NA, )
    montant = models.PositiveIntegerField()
    libelle = models.CharField( max_length=100, default='N.A')
    immatriculation = models.ForeignKey( Car, related_name='car', on_delete=models.CASCADE)
    etat_colis = models.CharField( max_length=10, choices=ETAT_CHOICES, default=ENVOYE, )
    emplacement = models.PositiveIntegerField(default=0 , validators=[MaxValueValidator(50),])
    #zone = models.TextField(default='RAS')
    observation = models.TextField()
    history = HistoricalRecords()

    objects = ColiManager()

    def __str__(self):
        return 'colis du {} , de {} a {}'.format(self.dateheure, self.telephone_exp, self.telephone_dest)

    class Meta:
        ordering = ['-dateheure']


class ColisFile(models.Model):

    file = models.FileField( upload_to="files/%Y/%m/%d", null=True, blank=True )
    coli = models.ForeignKey( Coli, on_delete=models.CASCADE )

    def __str__(self):
        return 'file {} '.format(self.coli)

