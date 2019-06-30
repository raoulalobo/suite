from django.contrib.auth.decorators import permission_required , login_required
from django.shortcuts import render , redirect
from .forms import ColiForm , ColiFileForm
from .models import Coli, ColisFile
from .filters import ColiFilter
from django.contrib import messages
import datetime
import requests
from django.db.models import Sum
from .tasks import order_created 
# Create your views here.

@login_required
def list_coli(request):

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

    montant = pneu_filter.qs.aggregate(Sum('montant'))['montant__sum'] or 0.00

    if 'req_coli' not in request.session :
        sess_req = False
    else :
        sess_req = True


    #request.session['pneu_filter'] = pneu_filter
    


    return render(request,'coli/list.html',{ 'colis': pneu_filter ,  'montant' :  montant } )

@login_required
def denied(request):
    
    return render(request,'coli/denied.html',{})

@login_required
def list_colis(request):

    colis = Coli.objects.all()
    
    return render(request,'coli/list.html',{ 'colis': colis })


@permission_required('colis_apps.can_add', login_url='/colis/accces-denied')
def add_coli(request):
    if request.method == 'POST':
        coli_form = ColiForm(request.POST )
        file_form = ColiFileForm( request.POST , request.FILES )
        files = request.FILES.getlist('file') 
        if coli_form.is_valid() and file_form.is_valid() :
            coli = coli_form.save()
            for f in files :
                #ajouter un tache avec celery ici
                file_instance = ColisFile(file=f, coli=coli )
                file_instance.save()

            #SMS avec Celery et RabbitMQ
            order_created.delay(coli.id)
            
                
            messages.success( request,'Item has been added')
            return redirect('colis_apps:list.coli')
    else:
        coli_form = ColiForm()
        file_form = ColiFileForm()

    return render(request,'coli/add.html',{'coli_form': coli_form , 'file_form' : file_form })

@permission_required('colis_apps.can_change', login_url='/colis/accces-denied')
def update_coli(request, coli_id ):
    item = Coli.objects.get( pk = coli_id )
    joint = ColisFile.objects.filter( coli = coli_id )
    coli_form = ColiForm(request.POST or None, instance=item )
    file_form = ColiFileForm( request.POST or None , request.FILES  )
    files = request.FILES.getlist('file')
    if coli_form.is_valid() and file_form.is_valid() :
        colicommit = coli_form.save(commit=False)
        coli = colicommit.save(update_fields=['etat_colis'])
        for f in files :
                file_instance = ColisFile(file=f, coli=colicommit )
                file_instance.save() 
        #SMS
        order_created.delay(colicommit.id)
            
        messages.success( request,'Item has been updated')
        return redirect('colis_apps:list.coli')
    else:
        coli_form = ColiForm( None,  instance=item )
        file_form = ColiFileForm()

    return render(request, 'coli/add.html', { 'coli_form': coli_form , 'file_form' : file_form , 'joint': joint })

@login_required
def detail_coli( request, coli_id ):
    
    item = Coli.objects.get( pk = coli_id )
    files = ColisFile.objects.filter( coli_id = coli_id )
    history = Coli.history.filter( id = coli_id ) 

    return render(request,'coli/detail.html',{'item': item , 'files': files  , 'history': history })

@permission_required('colis_apps.can_delete', login_url='/colis/accces-denied')
def delete( request, coli_id ):
    
    item = Coli.objects.get( pk = coli_id )
    files = ColisFile.objects.filter( coli_id = coli_id )

    return render(request,'coli/delete.html',{'item': item , 'files': files })

@permission_required('colis_apps.can_delete', login_url='/colis/accces-denied')
def delete_coli(request, coli_id ):
    item = Coli.objects.get( pk = coli_id )
    item.delete()
    messages.success( request,('Item has been deleted') )
    return redirect('colis_apps:list.coli')

@permission_required('colis_apps.can_delete', login_url='/colis/accces-denied')
def delete_file(request, file_id , coli_id ):
    item = ColisFile.objects.get( pk = file_id )
    item.delete()
    messages.success( request,'File has been deleted')
    return redirect('colis_apps:update.coli' , coli_id )