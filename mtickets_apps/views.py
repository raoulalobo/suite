from django.contrib.auth.decorators import permission_required , login_required
from django.shortcuts import render , redirect
from .models import Mticket, Partner
from django.contrib import messages
from django.db.models import Sum
from .filters import MticketFilter
from .forms import MticketForm
import datetime
import requests



# Create your views here.

@login_required
def list_mtickets(request):

    mticketss = Mticket.objects.all()
    mtickets = Mticket.objects.all().filter( dateheure__gte=datetime.date.today() ) 

    req_mticket = request.GET
    req_mticket_list_key = list(req_mticket.keys())
    req_mticket_list_value = list(req_mticket.values())
    req_mticket_list_len = len(req_mticket_list_key)

    
    if req_mticket_list_key :
    # Si les keys values existent ca veut dire q on clique sur la recherche    

        if not (  bool( req_mticket_list_value[2] ) and bool( req_mticket_list_value[3] ) ):
        # Si les champs dates sont vides filtrer les donnees sur la date du jour
            mticket_filter = MticketFilter( request.GET , queryset= mtickets )
        else:  
            mticket_filter = MticketFilter( request.GET , queryset= mticketss )
            
        request.session['req_mticket'] = request.GET

        
    if not req_mticket_list_key and (  'req_mticket' not in request.session ):
    # Si les keys values existent pas te q il ya pas de session req_pneu filter sur la date du jour
    # cas utilisation : retour vers la liste principale suite a un ajout, modification ou sppression apres recherche
        mticket_filter = MticketFilter( request.GET , queryset= mtickets )
    else :
    # Cas utilisation : Retour vers la liste principale suite a un ajout , modification ou suppression apres recherche    
        mticket_filter = MticketFilter( request.session['req_mticket'] , queryset= mticketss )

    if 'req_mticket' not in request.session :
        sess_req = False
    else :
        sess_req = True


    #request.session['pneu_filter'] = pneu_filter

    return render(request,'mticket/list.html',{ 'mtickets_query': mticket_filter } )


@permission_required('colis_apps.add_coli', login_url='colis_apps:denied')
def add_mticket(request):

    ##Ce a quoi mon code doit ressembler
    if request.method == 'POST':
        form = MticketForm( request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password was updated successfully!')  # <-
            return redirect('mtickets_apps:list.mtickets') 
        else:
            messages.warning(request, 'Please correct the error below.')  # <-
    else:
        form = MticketForm()

    ##Ancien code
    #if request.method == 'POST':
    #    mticket_form = MticketForm(request.POST )
    #    mticket_form.save()
    #    messages.success( request,'Item has been added')
    #    return redirect('mtickets_apps:list.coli')  
    #else:
    #    mticket_form = MticketForm()
        
    return render(request,'mticket/add_.html',{'mticket_form': form })


def update_mticket(request, _id ):
    item = Mticket.objects.get( pk = _id )
    form = MticketForm(request.POST or None, instance=item )
    history = Mticket.history.filter( id = _id )
    if form.is_valid():
        form.save()
        return redirect('mtickets_apps:list.mtickets')
    else:
        form = MticketForm( None,  instance=item )

    return render(request, 'mticket/add_.html', { 'mticket_form': form , 'history':history , 'update': True , 'item': item})


@login_required
def detail_mticket( request, mticket_id ):
    
    item = Mticket.objects.get( pk = mticket_id )
    history = Mticket.history.filter( id = mticket_id ) 

    return render(request,'mticket/detail.html',{'item': item , 'history': history })


@permission_required('colis_apps.delete_coli', login_url='colis_apps:denied')
def delete( request, mticket_id ):
    
    item = Mticket.objects.get( pk = mticket_id )

    return render(request,'mticket/delete.html',{'item': item })


@permission_required('colis_apps.delete_coli', login_url='colis_apps:denied')
def delete_mticket(request, mticket_id ):
    item = Mticket.objects.get( pk = mticket_id )
    item.delete()
    messages.success( request,('Item has been deleted') )
    return redirect('mtickets_apps:list.mtickets')



