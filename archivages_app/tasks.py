from celery import task
from django.core.mail import send_mail
from .models import Bleue
import requests
from celery.task.schedules import crontab
from celery.decorators import periodic_task
import datetime

#@periodic_task(run_every=(crontab(minute='*/2')), name="alertez", ignore_result=True)
@task
def alert():
    """
    Commentaires

    """
    liste = []
    dele = []
    dayz = []
    items  = Bleue.objects.all()
    for item in items :
        delta = item.date - datetime.datetime.now().date()
        d = delta.days
        if ( d <= 30 ) & ( d >0 ) :
            liste.append('{}({})'.format( item.cars.immatriculation , d ) )
            #dayz.append(item.cars.immatriculation)
        elif ( d <= 0 ) :
            dele.append('{}({})'.format( item.cars.immatriculation , d ) )
  

    if len(liste) != 0 :
            message = 'Moins de 30 jours pour expiration de carte grise de(s) vehicule(s) : {} '.format( liste )
            payload = {'action': 'sendmessage', 'username': 'FINEXS', 'password': 'Finexs12345', 'recipient': '237697509899' , 'messagetype':'SMS:TEXT', 'messagedata':message}
            r = requests.get("http://api.vassarl.com:9501/api", params=payload)


    if len(dele) != 0 :
            message = 'Vehicule(s) dont les donnees carte grise sont a supprimer : {} '.format( dele )
            payload = {'action': 'sendmessage', 'username': 'FINEXS', 'password': 'Finexs12345', 'recipient': '237697509899' , 'messagetype':'SMS:TEXT', 'messagedata':message}
            r = requests.get("http://api.vassarl.com:9501/api", params=payload)