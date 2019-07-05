from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

# Signal
class Profile(models.Model):

    #user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    user = models.OneToOneField( User ,on_delete=models.CASCADE)
    phone = models.CharField(max_length=30, blank=True ,null=True )
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/',blank=True,null=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# A  comprendre .
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()