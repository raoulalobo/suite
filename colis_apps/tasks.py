from celery import task
from django.core.mail import send_mail
from .models import Coli, ColisFile
from account.models import Profile
import requests



@task
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """

    coli = Coli.objects.get(id=order_id)
    if  coli.etat_colis == 'envoye' :
        message = 'Cher client proprietaire du #{}, votre colis {} est en route pour {}. Infos Yde:699755276 - infos Dla:656968928 -Plaintes:697509899; Ouvert du lun. au sam : 08h-19h'.format( coli.telephone_dest , coli.numero_colis, coli.destination )
        payload = {'action': 'sendmessage', 'username': 'FINEXS', 'password': 'Finexs12345', 'recipient': '237{}'.format(coli.telephone_dest) , 'messagetype':'SMS:TEXT', 'messagedata':message}
        r = requests.get("http://api.vassarl.com:9501/api", params=payload)

    return r

@task
def rapport_created(req, total_count , total_montant, yde_count , yde_montant, dla_count, dla_montant) :
    
    usr = Profile.objects.get( user= req)

    message = 'Total: {} colis,{} FCFA\n Yde: {} colis,{} FCFA\n '.format( total_count, total_montant, yde_count, yde_montant )
    payload = {'action': 'sendmessage', 'username': 'FINEXS', 'password': 'Finexs12345', 'recipient': '237{}'.format(usr.phone) , 'messagetype':'SMS:TEXT', 'messagedata':message}
    r = requests.get("http://api.vassarl.com:9501/api", params=payload)

    return r