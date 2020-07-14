from django.contrib.auth.decorators import permission_required , login_required
from django.shortcuts import render , redirect
from django.http import JsonResponse
from .forms import ColiForm , ColiFileForm , ClientForm
from .models import Coli, ColisFile, Profile, Client
from cars_app.models import Car
from .filters import ColiFilter , ClientFilter
from django.contrib import messages
import datetime
import requests
from django.db.models import Sum , Count , DateTimeField , DateField , TimeField
from .tasks import sms_coli , rapport_created
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.functions import TruncMonth , Extract , Trunc , TruncHour , TruncWeek
from django.core import serializers
import pickle

from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from dal import autocomplete 
import socket

from django.db.models import Q

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

# Create your views here.

def email_check(user):
    return user.email.endswith('@example.com')

def verify_group(user):
    return user.email.endswith('@example.com')

def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False

def one_time_startup() :

    liste = ['manager','management','colis','colis_admin','resa','resa_admin','scan','scan_admin']
    for name in liste : 
        try:
            group = Group.objects.get(name=name)
        except Group.DoesNotExist:
            group = Group.objects.create(name=name)

#django-autocomplete-light
class CountryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !

        qs = Car.objects.all()

        if self.q:
            qs = qs.filter(immatriculation__icontains=self.q)

        return qs

    def get_result_label(self, item):
        return item.immatriculation

class ClientPhoneAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !

        qs = Client.objects.all()

        if self.q:
            #qs = qs.filter(phone__icontains=self.q)
            qs = qs.filter( Q(phone__icontains=self.q) | Q(nom__icontains=self.q) )

        return qs

    def get_result_label(self, item):
        #return item.phone
        return '{}-{}'.format(item.phone , item.nom)

    #def get_result_value(self, item):
    #    return item.phone

class ClientNomAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !

        qs = Client.objects.all()

        id = self.forwarded.get('id', None)

        if id:
            #print('Telefonika : {} '.format(phone) )
            print('forwardGet_queryset : {} '.format( self.forwarded.get('id', None) ) )
            qs = qs.filter(id=id) 

        if self.q:
            qs = qs.filter(nom__icontains=self.q)

        return qs

    def get_result_label(self, item):
        return item.nom

    def create_object(self, text):

        print('create_field : {} '.format( self.create_field ) )

        print('forwardCreate_object : {} '.format( self.forwarded.get('id', None) ) )

        print('Text : {} '.format( text ) )

        clnt = Client.objects.get_or_create( id=self.forwarded.get('id', None) )[0]
        clnt.nom = text
        clnt.save()


        print('Clnt : {}'.format( clnt ) )

        """Create an object given a text."""
        return clnt



@login_required
def homeredirect(request):


    print('--------------------------------')
    print('colis_apps.view_coli : {}'.format( request.user.has_perm('colis_apps.view_coli') ) )
    print('--------------------------------')
    print('archivages_app.view_scan : {}'.format( request.user.has_perm('archivages_app.view_scan') ) )
    print('--------------------------------')
    print('mtickets_apps.view_mticket : {}'.format( request.user.has_perm('mtickets_apps.view_mticket') ) )
    print('--------------------------------')




    if request.user.has_perm('colis_apps.view_coli'):
        return redirect('colis_apps:list.coli')
    elif request.user.has_perm('archivages_app.view_scan'):
        return redirect('archivages_app:list.facture')
    elif request.user.has_perm('mtickets_apps.view_mticket'):
        return redirect('mtickets_apps:list.mtickets')
    else :
        return redirect('colis_apps:denied')

@login_required
def list_coli(request):

    pneuss = Coli.objects.all()
    pneus = Coli.objects.all().filter( dateheure__gte=datetime.date.today() ) 


    req_pneu = request.GET
    req_pneu_list_key = list(req_pneu.keys())
    req_pneu_list_value = list(req_pneu.values())
    req_pneu_list_len = len(req_pneu_list_key)

    req_session = request.session

    print('---------------req_session-----------------')
    print('req_session : {}'.format( request.session.keys() ) )

    print('---------------_auth_user_id-----------------')
    print('req_session : {}'.format( request.session['_auth_user_id'] ) )

    print('---------------_auth_user_backend-----------------')
    print('req_session : {}'.format( request.session['_auth_user_backend'] ) )

    print('---------------_auth_user_hash-----------------')
    print('req_session : {}'.format( request.session['_auth_user_hash'] ) )

    redis_coli = ''
    redis_coli = redis_coli + request.session['_auth_user_hash'] + socket.gethostname() + '_coli'

    print('---------------redis_coli-----------------')
    print('redis_coli : {}'.format( redis_coli ) )

    #print('--------------------------------')
    #print('req_pneu_list_key : {}'.format( req_pneu_list_key ) )
    #print('--------------------------------')
    #print('req_pneu_list_value : {}'.format( req_pneu_list_value ) )
    #print('--------------------------------')
    #print('req_pneu_list_len : {}'.format( req_pneu_list_len ) )
    #print('--------------------------------')
    #print('req_session.get("req_coli") : {}'.format( req_session.get('req_coli') ) )
    #print('--------------------------------')
    

    
    if req_pneu_list_len > 0 :
        date_lte = len( req_pneu.get('date_lte') )
        date_gte = len( req_pneu.get('date_gte') )
        #print('request.GET.date_lte : {}'.format( len( req_pneu.get('date_lte') ) == 0 ) )
        #print('request.GET.numero_colis : {}'.format( len( req_pneu.get('numero_colis') ) ) )
        # Si les keys values existent ca veut dire q on clique sur la recherche    
        if (  date_lte == 0 ) and ( date_gte == 0 ):
        # Si les champs dates sont vides filtrer les donnees sur la date du jour
            pneu_filter = ColiFilter( request.GET , queryset= pneus )
        else:  
            pneu_filter = ColiFilter( request.GET , queryset= pneuss )
            
        request.session['req_coli'] = request.GET


    if ( req_pneu_list_len == 0 ) and (  'req_coli' not in request.session ):
        #print('-------------------------------')
        #print('req_coli NOT IN request.session')
        # Si les keys values existent pas te q il ya pas de session req_pneu filter sur la date du jour
        # cas utilisation : retour vers la liste principale suite a un ajout, modification ou sppression apres recherche
        pneu_filter = ColiFilter( request.GET , queryset= pneus )


        
    if ( req_pneu_list_len == 0 ) and (  'req_coli' in request.session ):
        #print('-------------------------------')
        #print('req_coli in request.session')
        # Cas utilisation : Retour vers la liste principale suite a un ajout , modification ou suppression apres recherche    
        pneu_filter = ColiFilter( request.session['req_coli'] , queryset= pneuss )


    #print('--------------GroupBy------------------')
    test = pneu_filter.qs.annotate( month = Extract('coli_created_at' , 'day') ).values('month').annotate(Total=Sum('montant')).order_by() 
    test = test.values('month', 'Total')
    #print('test: {}'.format( test ) )
    
    
    montant = pneu_filter.qs.aggregate(Sum('montant'))['montant__sum'] or 0.00
    somme = sum( [item.montant for item in pneu_filter.qs]) or 0.00

    #print( '--------------Montant---------------------')
    #print( montant )

    #print( '--------------Somme---------------------')
    #print( somme )
    


    if 'req_coli' not in request.session :
        sess_req = False
    else :
        sess_req = True

    cache.set( redis_coli , pneu_filter.qs , timeout=CACHE_TTL)


    print( '--------------Redis---------------------')
    print( cache.get(redis_coli) )

    #user_list = User.objects.all()
    


    #hotel_list= pneu_filter.qs
    #json_hotel = serializers.serialize('json', hotel_list)
    #context={'hotel_list':json_hotel}


    equipments = [equipment.numero_colis for equipment in Coli.objects.all()]


    request.session['pneu_filter'] = equipments

    #print('request.session: {}'.format( request.session['pneu_filter'].values() ) )
    #print('request.session["pneu_filter"]: {}'.format( request.session['pneu_filter'] ) )
    #print('pneu_filter: {}'.format( pneu_filter.qs ) )

    return render(request,'coli/list.html',{ 'colis': pneu_filter ,  'montant' :  montant } )

def chart(request):

    return render(request,'coli/chart.html',{} )


@login_required
def chart_coli(request):

    redis_coli = ''
    redis_coli = redis_coli + request.session['_auth_user_hash'] + socket.gethostname() + '_coli'

    labels = []
    data = []

    chart = cache.get(redis_coli)

    print('chart: {}'.format( chart ) )
    #Ventes par jours de la semaine
    test = chart.annotate( week_day = Extract('dateheure' , 'week_day', output_field=DateTimeField() ) ).values('week_day').annotate(Total=Sum('montant')).order_by('week_day')

    #Tuples
    weekDays = ("Saturday","Sunday","Monday","Tuesday","Wednesday","Thursday","Friday")

    for entry in test:
        labels.append( weekDays[ int( entry['week_day'] ) ] )
        #labels.append(entry['month'].strftime("%H"))
        data.append(entry['Total'])

    #Vente par jours
    #test = chart.annotate( days = Trunc('coli_created_at' , 'day', output_field=DateTimeField() ) ).values('days').annotate(Total=Sum('montant')).order_by('days') 

    #for entry in test:
    #    labels.append(entry['days'].strftime("%a %d. %b %y"))
    #    #labels.append(entry['month'].strftime("%H"))
    #    data.append(entry['Total'])
    

    return JsonResponse(data={'labels': labels,'data': data,})


@login_required
def chart_coli_heure(request):

    redis_coli = ''
    redis_coli = redis_coli + request.session['_auth_user_hash'] + socket.gethostname() + '_coli'

    labels = []
    data = []

    chart = cache.get(redis_coli)

    print('chart: {}'.format( chart ) )

    test = chart.annotate( day = TruncHour('dateheure' , output_field=TimeField() ) ).values('day').annotate(Total=Sum('montant')).order_by('day') 

    for entry in test:
        #labels.append(entry['month'].strftime("%a %d. %b %y"))
        labels.append(entry['day'].strftime("%H"))
        data.append(entry['Total'])
    

    return JsonResponse(data={'labels': labels,'data': data,})



def list_client(request):

    clientss = Client.objects.all()
    clients = Client.objects.all().filter( client_created_at__gte=datetime.date.today() ) 


    req_client = request.GET
    req_client_list_key = list(req_client.keys())
    req_client_list_value = list(req_client.values())
    req_client_list_len = len(req_client_list_key)

    req_session = request.session


    
    if req_client_list_len > 0 :
        date_lte = len( req_client.get('date_lte') )
        date_gte = len( req_client.get('date_gte') )

        # Si les keys values existent ca veut dire q on clique sur la recherche    
        if (  date_lte == 0 ) and ( date_gte == 0 ):
        # Si les champs dates sont vides filtrer les donnees sur la date du jour
            client_filter = ClientFilter( request.GET , queryset= clients )
        else:  
            client_filter = ClientFilter( request.GET , queryset= clientss )
            
        request.session['req_client'] = request.GET


    if ( req_client_list_len == 0 ) and (  'req_client' not in request.session ):
        # Si les keys values existent pas te q il ya pas de session req_pneu filter sur la date du jour
        # cas utilisation : retour vers la liste principale suite a un ajout, modification ou sppression apres recherche
        client_filter = ClientFilter( request.GET , queryset= clients )


        
    if ( req_client_list_len == 0 ) and (  'req_client' in request.session ):
        # Cas utilisation : Retour vers la liste principale suite a un ajout , modification ou suppression apres recherche    
        client_filter = ClientFilter( request.session['req_client'] , queryset= clientss )


    return render(request,'client/list.html',{ 'clients': client_filter } )



@login_required
def denied(request):
    
    return render(request,'coli/denied.html',{})

@login_required
def list_colis(request):

    colis = Coli.objects.all()
    
    return render(request,'coli/list.html',{ 'colis': colis })

@permission_required('colis_apps.add_coli', login_url='colis_apps:denied')
def add_coli(request):
    data = dict()

    if request.method == 'POST':
        coli_form = ColiForm(request.POST )
        file_form = ColiFileForm( request.POST , request.FILES )
        files = request.FILES.getlist('file') 
        if coli_form.is_valid() and file_form.is_valid() :
            coli = coli_form.save()
            for f in files :
                file_instance = ColisFile(file=f, coli=coli )
                file_instance.save()

            #Envoie de SMS avec Celery et RabbitMQ
            sms_coli.delay( coli.id , request.user.username )

            #Django message    
            #messages.success( request,'Item has been added')

            current_user_groups = request.user.groups.values_list('name', flat=True)
            
            if 'douala' in current_user_groups  :
                return redirect('colis_apps:detail.coli', coli.id )
            else :
                return redirect('colis_apps:list.coli') 

        
    else:
        coli_form = ColiForm()
        file_form = ColiFileForm()

    return render(request,'coli/add.html',{'coli_form': coli_form , 'file_form' : file_form })

def add_client(request):
    data = dict()

    if request.method == 'POST':
        client_form = ClientForm(request.POST )
        if client_form.is_valid() :
            client = client_form.save()

            messages.success( request,'Item has been added')

            return redirect('colis_apps:add.client') 

    else:
        client_form = ClientForm()

    return render(request,'client/add.html',{'client_form': client_form  })

@permission_required('colis_apps.view_coli', login_url='colis_apps:denied')
def update_coli(request, coli_id ):
    item = Coli.objects.get( pk = coli_id )
    #joint = ColisFile.objects.filter( coli = coli_id )
    joint = item.colisfile_set.all()
    coli_form = ColiForm(request.POST or None, instance=item )
    file_form = ColiFileForm( request.POST or None , request.FILES  )
    files = request.FILES.getlist('file')
    history = Coli.history.filter( id = coli_id )

    if coli_form.is_valid() and file_form.is_valid() :
        colicommit = coli_form.save(commit=False)

        if request.user.has_perm('colis_apps.delete_coli'):
        #if request.user.groups.filter(name = 'colis_admin').exists():
            coli = colicommit.save()
            print('Coli colis_apps.delete_coli : {}'.format( coli ) )
            print('--------------------------------')
        #else:
        #    coli = colicommit.save(update_fields=['etat_colis', 'emplacement'])
       
        if request.user.has_perm('colis_apps.change_coli'):
            coli = colicommit.save(update_fields=['immatriculation','etat_colis', 'emplacement'])
            

        for f in files :
                file_instance = ColisFile(file=f, coli=colicommit )
                file_instance.save()

        #Envoie de SMS avec Celery et RabbitMQ
        sms_coli.delay(colicommit.id , request.user.username )
            
        messages.success( request,'Item has been updated')

        current_user_groups = request.user.groups.values_list('name', flat=True)
            
        if 'douala' in current_user_groups  :
            print('Coli : {}'.format( coli ) )
            print('--------------------------------')
            return redirect('colis_apps:detail.coli', coli_id )
        else :
            return redirect('colis_apps:list.coli') 

    else:
        coli_form = ColiForm( None,  instance=item )
        file_form = ColiFileForm()

    return render(request, 'coli/add.html', { 'coli_form': coli_form , 'file_form' : file_form , 'joint': joint , 'history': history, 'item': item, 'update': True })

@login_required
def detail_coli( request, coli_id ):
    
    item = Coli.objects.get( pk = coli_id )
    files = item.colisfile_set.all()
    #files = ColisFile.objects.filter( coli_id = coli_id )
    history = Coli.history.filter( id = coli_id ) 

    return render(request,'coli/detail_.html',{'item': item , 'files': files  , 'history': history })

@login_required
def client_coli( request, client_id ):

    item = Client.objects.get( pk = client_id )
    colis = item.telephone_exp.all()

                
    print('-----------get_coli------------------')
    print( colis )
    
    #envoyes = Coli.objects.filter( telephone_exp = client_id ) 
    #recus = Coli.objects.filter( telephone_dest = client_id )

    #last_envoye = envoyes[0].dateheure

    return render(request,'client/detail.html',{'item': item , 'colis': colis })
    #return render(request,'client/coli.html',{'envoyes': envoyes  , 'recus' : recus , 'last_envoye' : last_envoye  })


@permission_required('colis_apps.delete_coli', login_url='colis_apps:denied')
def delete( request, coli_id ):
    
    item = Coli.objects.get( pk = coli_id )
    files = ColisFile.objects.filter( coli_id = coli_id )

    return render(request,'coli/delete.html',{'item': item , 'files': files })

@permission_required('colis_apps.delete_coli', login_url='colis_apps:denied')
def delete_coli(request, coli_id ):
    item = Coli.objects.get( pk = coli_id )
    item.delete()
    messages.success( request,('Item has been deleted') )
    return redirect('colis_apps:list.coli')

@permission_required('colis_apps.delete_coli', login_url='colis_apps:denied')
def delete_file(request, file_id , coli_id ):
    item = ColisFile.objects.get( pk = file_id )
    item.delete()
    messages.success( request,'File has been deleted')
    return redirect('colis_apps:update.coli' , coli_id )

@login_required
def rapport_coli(request):

    pneuss = Coli.objects.all()
    pneus = Coli.objects.all().filter( dateheure__gte=datetime.date.today() ) 

    req_pneu = request.GET
    req_pneu_list_key = list(req_pneu.keys())
    req_pneu_list_value = list(req_pneu.values())
    req_pneu_list_len = len(req_pneu_list_key)

    
    if req_pneu_list_key :
    # Si les keys values existent ca veut dire q on clique sur la recherche    

        if not (  bool( req_pneu_list_value[2] ) and bool( req_pneu_list_value[3] ) ):
        # Si les champs dates sont vides filtrer les donnees sur la date du jour
            pneu_filter = ColiFilter( request.GET , queryset= pneus )
        else:  
            pneu_filter = ColiFilter( request.GET , queryset= pneuss )
            
        request.session['req_coli'] = request.GET

        
    if not req_pneu_list_key and (  'req_coli' not in request.session ):
    # Si les keys values existent pas te q il ya pas de session req_pneu filter sur la date du jour
    # cas utilisation : retour vers la liste principale suite a un ajout, modification ou sppression apres recherche
        pneu_filter = ColiFilter( request.GET , queryset= pneus )
    else :
    # Cas utilisation : Retour vers la liste principale suite a un ajout , modification ou suppression apres recherche    
        pneu_filter = ColiFilter( request.session['req_coli'] , queryset= pneuss )

    total_count = pneu_filter.qs.count()
    total_montant = pneu_filter.qs.aggregate(Sum('montant'))['montant__sum'] or 0.00

    yde_count = (pneu_filter.qs).filter(destination='DLA').count()
    yde_montant =  (pneu_filter.qs).filter(destination='DLA').aggregate(Sum('montant'))['montant__sum'] or 0.00
    
    dla_count = (pneu_filter.qs).filter(destination='YDE').count()
    dla_montant =  (pneu_filter.qs).filter(destination='YDE').aggregate(Sum('montant'))['montant__sum'] or 0.00

    rapport_created.delay( request.user.id , total_count, total_montant, yde_count, yde_montant, dla_count, dla_montant )

    if 'req_coli' not in request.session :
        sess_req = False
    else :
        sess_req = True
    

    return redirect('colis_apps:list.coli')