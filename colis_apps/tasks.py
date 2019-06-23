from celery import task
from django.core.mail import send_mail
from .models import Coli, ColisFile
import requests



@task
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """

    coli = Coli.objects.get(id=order_id)
    if  coli.etat_colis == 'envoye' :
        message = 'Cher client, votre colis #{} est en route pour {}. Infos Yde:699755276 - infos Dla:656968928 -Plaintes:697509899; Ouvert du lun. au sam : 08h-19h'.format( coli.numero_colis, coli.destination )
        payload = {'action': 'sendmessage', 'username': 'FINEXS', 'password': 'Finexs12345', 'recipient': coli.telephone_dest , 'messagetype':'SMS:TEXT', 'messagedata':message}
        r = requests.get("http://api.vassarl.com:9501/api", params=payload)

    return coli.numero_colis
