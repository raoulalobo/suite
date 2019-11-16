from celery import task
from django.core.mail import send_mail
from .models import Coli, ColisFile
from .models import Profile
import requests



@task
def order_created(order_id):


    coli = Coli.objects.get(id=order_id)
    if  coli.etat_colis == 'envoye' :
        message = 'Cher client proprietaire du #{}, votre colis {} est en route pour {}. Montant paye : {} .Yde:699755276 ,Dla:656968928 -Plaintes:697509899 ( SMS )'.format( coli.telephone_exp , coli.numero_colis, coli.destination, coli.montant )
        payload = {'action': 'sendmessage', 'username': 'FINEXS', 'password': 'Finexs12345', 'recipient': '237{}'.format(coli.telephone_exp) , 'messagetype':'SMS:TEXT', 'messagedata':message}
        r = requests.get("http://api.vassarl.com:9501/api", params=payload)

    if coli.etat_colis == 'nontrouve' :
        message = 'ALERTE: Le colis #{} est introuvable a {}. Montant paye : {} , Valeur declaree : {} .'.format( coli.numero_colis, coli.destination, coli.montant , coli.valeur_declaree)
        payload = {'action': 'sendmessage', 'username': 'FINEXS', 'password': 'Finexs12345', 'recipient': '237697509899,237656806999,696669942' , 'messagetype':'SMS:TEXT', 'messagedata':message}
        r = requests.get("http://api.vassarl.com:9501/api", params=payload)

    return r

@task
def rapport_created(req, total_count , total_montant, yde_count , yde_montant, dla_count, dla_montant) :
    
    usr = Profile.objects.get( user= req)

    message = 'Total: {} colis,{} FCFA\n Yde: {} colis,{} FCFA\n Dla: {} colis,{} FCFA '.format( total_count, total_montant, yde_count, yde_montant, dla_count , dla_montant)
    payload = {'action': 'sendmessage', 'username': 'FINEXS', 'password': 'Finexs12345', 'recipient': '237{}'.format(usr.phone) , 'messagetype':'SMS:TEXT', 'messagedata':message}
    r = requests.get("http://api.vassarl.com:9501/api", params=payload)

    return r