from django.shortcuts import render
from .models import Facture, Bordereau, Bleue, Assurance, ScanFichier
from django.contrib import messages
from .forms import FactureForm , ScanFichierForm , BordereauForm,  BleueForm 
from django.shortcuts import render , redirect
from .filters import FactureFilter, BordereauFilter, BleueFilter
import datetime
from django.db.models import Sum
from .utils import rosine

# Create your views here.

#--------------------------------------------------------------------------------------#

def list_facture(request):

    item_filter = rosine(request,Facture,FactureFilter,'req_facture')

    montant = item_filter.qs.aggregate(Sum('montant'))['montant__sum'] or 0.00
    
    #Export CSV . Mais pq ne pas utiliser cette vue pour l'url export csv ?
    #request.session['pneu_filter'] = pneu_filter

    return render(request,'archivage/list.html',{ 'bordereau_pages':'active','factures': item_filter , 'montant': montant  } )

def add_facture(request):
    if request.method == 'POST':
        facture_form = FactureForm(request.POST )
        file_form = ScanFichierForm( request.POST , request.FILES )
        files = request.FILES.getlist('file') 
        if facture_form.is_valid() and file_form.is_valid() :
            facture = facture_form.save()
            for f in files :
                #ajouter un tache avec celery ici
                file_instance = ScanFichier( file=f, scanfichier=facture )
                file_instance.save()

            #SMS avec Celery et RabbitMQ
            #order_created.delay(coli.id)
            
                
            messages.success( request,'Item has been added')
            return redirect('archivages_app:list.facture')
    else:
        facture_form = FactureForm()
        file_form = ScanFichierForm()

    return render(request,'archivage/add.html',{'form': facture_form , 'file_form' : file_form })

#@permission_required('colis_apps.change_coli', login_url='colis_apps:denied')
def update_facture(request, _id ):

    item = Facture.objects.get( pk = _id )
    joint = ScanFichier.objects.filter( scanfichier = _id )
    form = FactureForm(request.POST or None, instance=item )
    file_form = ScanFichierForm( request.POST or None , request.FILES  )
    files = request.FILES.getlist('file')
    history = Facture.history.filter( id = _id )

    if form.is_valid() and file_form.is_valid() :
        commit = form.save(commit=False)

        if request.user.has_perm('colis_apps.delete_coli'):
            facture = commit.save()
        else:
            facture = commit.save(update_fields=['observation'])

        for f in files :
                file_instance = ScanFichier(file=f, scanfichier=_id )
                file_instance.save() 
       
            
        messages.success( request,'Item has been updated')
        return redirect('archivages_app:list.facture')
    else:
        form = FactureForm( None,  instance=item )
        file_form = ScanFichierForm()


    return render(request, 'archivage/add.html', { 'form': form , 'file_form' : file_form , 'joint': joint , 'history': history, 'item': item, 'update': True })

#@permission_required('colis_apps.delete_coli', login_url='colis_apps:denied')
def delete_facture(request, _id ):
    item = Facture.objects.get( pk = _id )
    item.delete()
    messages.success( request,('Item has been deleted') )
    return redirect('archivages_app:list.facture')

#@permission_required('colis_apps.delete_coli', login_url='colis_apps:denied')
def delete_file_facture(request, file_id , _id ):
    item = ScanFichier.objects.get( pk = file_id )
    item.delete()
    messages.success( request,'File has been deleted')
    return redirect('archivages_app:update.facture' , _id )

    #------------------------------------------------------------------------#

#---------------------------------------------------------------------------------------#

def list_bordereau(request):

    #itemss = Bordereau.objects.all()
    #items = Bordereau.objects.all().filter( date__gte=datetime.date.today() ) 
    
    item_filter = rosine( request, Bordereau , BordereauFilter , 'req_bordereau' )

    #request.session['pneu_filter'] = pneu_filter

    return render(request,'bordereau/list.html',{ 'bordereau_pages':'active' , 'items': item_filter  } )


def add_bordereau(request):
    if request.method == 'POST':
        form = BordereauForm(request.POST )
        file_form = ScanFichierForm( request.POST , request.FILES )
        files = request.FILES.getlist('file') 
        if form.is_valid() and file_form.is_valid() :
            bordereau = form.save()
            for f in files :
                file_instance = ScanFichier(file=f, scanfichier=bordereau )
                file_instance.save()

            #ajouter un tache avec celery ici
            #SMS avec Celery et RabbitMQ
            #order_created.delay(coli.id)
            
                
            messages.success( request,'Item has been added')
            return redirect('archivages_app:list.bordereau')
    else:
        form = BordereauForm()
        file_form = ScanFichierForm()

    return render(request,'bordereau/add.html',{'form': form , 'file_form' : file_form })

#@permission_required('colis_apps.change_coli', login_url='colis_apps:denied')
def update_bordereau(request, _id ):
    item = Bordereau.objects.get( pk = _id )
    joint = ScanFichier.objects.filter( scanfichier = _id )
    form = BordereauForm(request.POST or None, instance=item )
    file_form = ScanFichierForm( request.POST or None , request.FILES  )
    files = request.FILES.getlist('file')
    history = Bordereau.history.filter( id = _id )

    if form.is_valid() and file_form.is_valid() :
        commit = form.save(commit=False)

        if request.user.has_perm('colis_apps.delete_coli'):
            bordereau = commit.save()
        else:
            bordereau = commit.save(update_fields=['etat_colis', 'emplacement'])

        for f in files :
                file_instance = ScanFichier(file=f, scanfichier_id= _id )
                file_instance.save() 
       
            
        messages.success( request,'Item has been updated')
        return redirect('archivages_app:list.bordereau')
    else:
        form = BordereauForm( None,  instance=item )
        file_form = ScanFichierForm()

    return render(request, 'bordereau/add.html', { 'form': form , 'file_form' : file_form , 'joint': joint , 'history': history, 'item': item, 'update': True })

#@permission_required('colis_apps.delete_coli', login_url='colis_apps:denied')
def delete_bordereau(request, _id ):
    item = Bordereau.objects.get( pk = _id )
    item.delete()
    messages.success( request,('Item has been deleted') )
    return redirect('archivages_app:list.bordereau')

#@permission_required('colis_apps.delete_coli', login_url='colis_apps:denied')
def delete_file_bordereau(request, file_id , _id ):
    item = ScanFichier.objects.get( pk = file_id )
    item.delete()
    messages.success( request,'File has been deleted')
    return redirect('archivages_app:update.bordereau' , _id )

#----------------------------------------------------------------------------------------#

def list_bleue(request):

    itemss = Bleue.objects.all()
    items = Bleue.objects.all().filter( dateheure__gte=datetime.date.today() ) 
    
    item_filter = rosine( request, Bleue , BleueFilter , 'req_bleue' )

    #request.session['pneu_filter'] = pneu_filter

    return render(request,'bleue/list.html',{ 'items': item_filter  } )

def add_bleue(request):

    if request.method == 'POST':
        form = BleueForm(request.POST )
        file_form = ScanFichierForm( request.POST , request.FILES )
        files = request.FILES.getlist('file') 
        if form.is_valid() and file_form.is_valid() :
            bleue = form.save()
            for f in files :
                file_instance = ScanFichier(file=f, content_object= bleue )
                file_instance.save()

            #ajouter un tache avec celery ici
            #SMS avec Celery et RabbitMQ
            #order_created.delay(coli.id)
            
                
            messages.success( request,'Item has been added')
            return redirect('archivages_app:list.bleue')
    else:
        form = BleueForm()
        file_form = ScanFichierForm()

    return render(request,'bleue/add.html',{'form': form , 'file_form' : file_form })

#@permission_required('colis_apps.change_coli', login_url='colis_apps:denied')
def update_bleue(request, _id ):
    item = Bleue.objects.get( pk = _id )
    joint = ScanFichier.objects.filter( bleue = _id )
    form = BleueForm(request.POST or None, instance=item )
    file_form = ScanFichierForm( request.POST or None , request.FILES  )
    files = request.FILES.getlist('file')
    history = Bleue.history.filter( id = _id )

    if form.is_valid() and file_form.is_valid() :
        commit = form.save(commit=False)

        if request.user.has_perm('colis_apps.delete_coli'):
            commitsave = commit.save()
        else:
            commitsave = commit.save(update_fields=['cars'])

        for f in files :
                file_instance = ScanFichier(file=f,  content_object= commit  )
                file_instance.save() 
       
            
        messages.success( request,'Item has been updated')
        return redirect('archivages_app:list.bleue')
    else:
        form = BleueForm( None,  instance=item )
        file_form = ScanFichierForm()

    #delta = datetime.datetime.now().date() - item.date
    #d = delta.days

    return render(request, 'bleue/add.html', { 'form': form , 'file_form' : file_form , 'joint': joint , 'history': history, 'item': item, 'update': True })

#@permission_required('colis_apps.delete_coli', login_url='colis_apps:denied')
def delete_bleue(request, _id ):
    item = Bleue.objects.get( pk = _id )
    item.delete()
    messages.success( request,('Item has been deleted') )
    return redirect('archivages_app:list.bleue')

#@permission_required('colis_apps.delete_coli', login_url='colis_apps:denied')
def delete_file_bleue(request, file_id , _id ):
    item = ScanFichier.objects.get( pk = file_id )
    item.delete()
    messages.success( request,'File has been deleted')
    return redirect('archivages_app:update.bleue' , _id )

