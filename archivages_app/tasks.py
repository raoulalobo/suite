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
    list = []
    items  = Bleue.objects.all()
    for item in items :
        delta = item.date - datetime.datetime.now().date()
        d = delta.days
        if ( d == 30 ):
            list.append(item.cars.immatriculation)
            message = '30 jours pour expiration de(s) vehicule(s) : {} '.format( list )
            payload = {'action': 'sendmessage', 'username': 'FINEXS', 'password': 'Finexs12345', 'recipient': '237697509899' , 'messagetype':'SMS:TEXT', 'messagedata':message}
            r = requests.get("http://api.vassarl.com:9501/api", params=payload)
        else :
            message = 'RAS'
            payload = {'action': 'sendmessage', 'username': 'FINEXS', 'password': 'Finexs12345', 'recipient': '237697509899' , 'messagetype':'SMS:TEXT', 'messagedata':message}
            r = requests.get("http://api.vassarl.com:9501/api", params=payload)
   


