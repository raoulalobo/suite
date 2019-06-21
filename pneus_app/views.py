import datetime
import requests
from .models import Pneu
from .forms import PneuForm
from .filters import PneuFilter
from django.contrib import messages
from .resources import PneuResource
from django.shortcuts import render , redirect
from django.http import HttpResponse, JsonResponse


# Cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache

# Settings
from django.conf import settings


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

# Create your views here.

def list_pneus(request):

    pneuss = Pneu.objects.all()
    pneus = Pneu.objects.all().filter( date__gte=datetime.date.today() ) 

    req_pneu = request.GET
    req_pneu_list_key = list(req_pneu.keys())
    req_pneu_list_value = list(req_pneu.values())
    req_pneu_list_len = len(req_pneu_list_key)

    
    if req_pneu_list_key :
    # Si les keys values existent ca veut dire q on clique sur la recherche    

        if  (  ( req_pneu_list_value[1] == '' ) and ( req_pneu_list_value[2] == '' ) ):
        # Si les champs dates sont vides filtrer les donnees sur la date du jour
            pneu_filter = PneuFilter( request.GET , queryset= pneus )
        else:  
            pneu_filter = PneuFilter( request.GET , queryset= pneuss )
            
        request.session['req_pneu'] = request.GET

        
    if not req_pneu_list_key and (  'req_pneu' not in request.session ):
    # Si les keys values existent pas te q il ya pas de session req_pneu filter sur la date du jour
    # cas utilisation : retour vers la liste principale suite a un ajout, modification ou sppression apres recherche
        pneu_filter = PneuFilter( request.GET , queryset= pneus )
    else :
    # Cas utilisation : Retour vers la liste principale suite a un ajout , modification ou suppression apres recherche    
        pneu_filter = PneuFilter( request.session['req_pneu'] , queryset= pneuss )

    if 'req_pneu' not in request.session :
        sess_req = False
    else :
        sess_req = True

    # Cache
    cache.set('pneu_filter', pneu_filter.qs , timeout=CACHE_TTL)


    
    return render(request,'pneu/list.html',{ 'pneus': pneu_filter ,'sess_req': sess_req , 'req': req_pneu_list_value , 'sess' : request.session.get('req_pneu') })


def add_pneu(request):

    #if ( 'req_pneu' in request.session  ):
    #    del request.session['req_pneu']

    if request.method == 'POST':
        pneu_form = PneuForm( request.POST ) 
        if pneu_form.is_valid() :
            pneu_form.save()
            return redirect('pneus_app:list.pneu')
    else:
        pneu_form = PneuForm()

    return render(request,'pneu/add.html',{'pneu_form': pneu_form  } )


def update_pneu(request, pneu_id ):
    item = Pneu.objects.get( pk = pneu_id )
    pneu_form = PneuForm(request.POST or None, instance=item )
    if pneu_form.is_valid() :
        pneu_form.save()
        return redirect('pneus_app:list.pneu')
    else:
        pneu_form = PneuForm( None,  instance=item )

    return render(request, 'pneu/add.html', { 'pneu_form': pneu_form })



def detail_pneu(request, pneu_id ):
    
    item = Pneu.objects.get( pk = pneu_id )

    return render(request,'pneu/detail.html',{'item': item })


def export(request):

    pneuss = Pneu.objects.all()
    pneus = Pneu.objects.all().filter( date__gte=datetime.date.today() ) 

    req_pneu = request.GET
    req_pneu_list_key = list(req_pneu.keys())
    req_pneu_list_value = list(req_pneu.values())
    req_pneu_list_len = len(req_pneu_list_key)

    
    if req_pneu_list_key :
    # Si les keys values existent ca veut dire q on clique sur la recherche    

        if not (  bool( req_pneu_list_value[2] ) or bool( req_pneu_list_value[3] ) ):
        # Si les champs dates sont vides filtrer les donnees sur la date du jour
            pneu_filter = PneuFilter( request.GET , queryset= pneus )
        else:  
            pneu_filter = PneuFilter( request.GET , queryset= pneuss )
            
        request.session['req_pneu'] = request.GET

        
    if not req_pneu_list_key and (  'req_pneu' not in request.session ):
    # Si les keys values existent pas te q il ya pas de session req_pneu filter sur la date du jour
    # cas utilisation : retour vers la liste principale suite a un ajout, modification ou sppression apres recherche
        pneu_filter = PneuFilter( request.GET , queryset= pneus )
    else :
    # Cas utilisation : Retour vers la liste principale suite a un ajout , modification ou suppression apres recherche    
        pneu_filter = PneuFilter( request.session['req_pneu'] , queryset= pneuss )

 

    pneu_resource = PneuResource()
    dataset = pneu_resource.export( request.session['pfff'] )
    
    #Export XLS
    #response = HttpResponse(dataset.csv, content_type='text/csv')
    #response['Content-Disposition'] = 'attachment; filename="export.csv"'
    
    #Export CSV
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="export.xls"'

    #email = EmailMessage('Subject of the Email', 'Body of the email', 'finexs-informatique@finexsvoyages.net', ['nathanaelalobo@gmail.com'])
    #email.attach('design.xls', dataset.xls,'application/vnd.ms-excel')
    #email.send()
    
    return response
