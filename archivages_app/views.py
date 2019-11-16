from django.shortcuts import render
from .models import Facture, Bordereau, Bleue, Assurance, ScanFichier, Plainte
from django.contrib import messages
from .forms import PlainteForm, FactureForm , ScanFichierForm , BordereauForm,  BleueForm , AssuranceForm
from django.shortcuts import render , redirect
from .filters import FactureFilter, BordereauFilter, BleueFilter, AssuranceFilter , PlainteFilter
import datetime
from django.db.models import Sum
from .utils import rosine , ajout_de_scans , mise_a_jour_scans , suppression_scan , suppression_scan_fichier

# Create your views here.

#--------------------------------------------------------------------------------------#

def list_facture(request):

    item_filter = rosine(request,Facture,FactureFilter,'req_facture')

    montant = item_filter.qs.aggregate(Sum('montant'))['montant__sum'] or 0.00
    
    #Export CSV . Mais pq ne pas utiliser cette vue pour l'url export csv ?
    #request.session['pneu_filter'] = pneu_filter

    return render(request,'facture/list.html',{ 'bordereau_pages':'active','factures': item_filter , 'montant': montant  } )

def add_facture(request):

    return ajout_de_scans( request, FactureForm , ScanFichierForm, ScanFichier, 'facture'  )

#@permission_required('colis_apps.change_coli', login_url='colis_apps:denied')
def update_facture(request, _id ):
    
    return mise_a_jour_scans( request, _id, Facture, ScanFichier, FactureForm, ScanFichierForm, 'colis_apps.delete_coli', 'observation','facture' )

    
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

#---------------------------------------------------------------------------------------#

def list_bordereau(request):
    
    item_filter = rosine( request, Bordereau , BordereauFilter , 'req_bordereau' )

    return render(request,'bordereau/list.html',{ 'bordereau_pages':'active' , 'items': item_filter  } )

def add_bordereau(request):
    
    return ajout_de_scans(request, BordereauForm, ScanFichierForm, ScanFichier , 'bordereau')

#@permission_required('colis_apps.change_coli', login_url='colis_apps:denied')
def update_bordereau(request, _id ):
    
    return mise_a_jour_scans( request, _id, Bordereau, ScanFichier, BordereauForm, ScanFichierForm, 'colis_apps.delete_coli', 'observatioin', 'bordereau')

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

    item_filter = rosine(request,Bleue,BleueFilter,'req_bleue')

    return render(request,'bleue/list.html',{ 'items': item_filter  } )

def add_bleue(request):

    return ajout_de_scans( request , BleueForm , ScanFichierForm , ScanFichier , 'bleue')

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

#----------------------------------------------------------------------------------------#
def list_assurance(request):

    item_filter = rosine( request, Assurance , AssuranceFilter , 'req_assurance')

    return render( request,'assurance/list.html',{'items': item_filter } )

def add_assurance(request) :

    return ajout_de_scans( request, AssuranceForm , ScanFichierForm, ScanFichier, 'assurance')

def update_assurance(request, _id):

    return mise_a_jour_scans( request , _id , Assurance , ScanFichier , AssuranceForm, ScanFichierForm , 'colis_apps.delete_coli','observation', 'assurance')

def delete_assurance( request , _id ):

    return suppression_scan ( request , _id , Assurance , 'assurance')

def delete_file_assurance( request , file_id , _id ):

    return suppression_scan_fichier ( request , file_id , _id , ScanFichier , 'assurance')


#------------------------------------------------------------------------------------------#

def list_plainte(request):

    item_filter = rosine( request , Plainte , PlainteFilter , 'req_plainte')

    return render( request,'plainte/list.html',{'items': item_filter } )

def add_plainte(request):
    return ajout_de_scans( request , PlainteForm , ScanFichierForm , ScanFichier , 'plainte')

def update_plainte(request, _id):
    return mise_a_jour_scans( request , _id, Plainte , ScanFichier, PlainteForm, ScanFichierForm, 'colis_apps.delete_coli', 'observation', 'plainte')

def delete_plainte( request , _id ):
    return suppression_scan ( request, _id, Plainte , 'plainte')

def delete_file_plainte ( request , file_id , _id ):
    return suppression_scan_fichier ( request , file_id, _id, ScanFichier , 'plainte')