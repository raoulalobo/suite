from django.shortcuts import render
from .models import Facture, Bordereau, Bleue, Assurance, ScanFichier, Plainte
from django.contrib import messages
from .forms import PlainteForm, FactureForm , ScanFichierForm , BordereauForm,  BleueForm , AssuranceForm
from django.shortcuts import render , redirect
from .filters import FactureFilter, BordereauFilter, BleueFilter, AssuranceFilter , PlainteFilter
import datetime
from django.db.models import Sum
from .utils import rosine , ajout_de_scans , mise_a_jour_scans , suppression_scan , suppression_scan_fichier
from django.contrib.auth.decorators import permission_required , login_required

# Create your views here.
#--------------------------------------------------------------------------------------#

@permission_required('archivages_app.view_scan', login_url='colis_apps:denied')
def list_facture(request):

    item_filter = rosine(request,Facture,FactureFilter,'req_facture')

    montant = item_filter.qs.aggregate(Sum('montant'))['montant__sum'] or 0.00
    
    #Export CSV . Mais pq ne pas utiliser cette vue pour l'url export csv ?
    #request.session['pneu_filter'] = pneu_filter

    return render(request,'facture/list.html',{ 'bordereau_pages':'active','factures': item_filter , 'montant': montant  } )

@permission_required('archivages_app.add_scan', login_url='colis_apps:denied')
def add_facture(request):

    return ajout_de_scans( request, FactureForm , ScanFichierForm, ScanFichier, 'facture'  )

@permission_required('archivages_app.view_scan', login_url='colis_apps:denied')
def update_facture(request, _id ):
    
    return mise_a_jour_scans( request, _id, Facture, ScanFichier, FactureForm, ScanFichierForm, 'archivages_app.change_scan', 'observation','facture' )
    
@permission_required('archivages_app.delete_scan', login_url='colis_apps:denied')
def delete_facture(request, _id ):
    item = Facture.objects.get( pk = _id )
    item.delete()
    messages.success( request,('Item has been deleted') )
    return redirect('archivages_app:list.facture')

@permission_required('archivages_app.delete_scan', login_url='colis_apps:denied')
def delete_file_facture(request, file_id , _id ):
    item = ScanFichier.objects.get( pk = file_id )
    item.delete()
    messages.success( request,'File has been deleted')
    return redirect('archivages_app:update.facture' , _id )

#---------------------------------------------------------------------------------------#

@permission_required('archivages_app.view_scan', login_url='colis_apps:denied')
def list_bordereau(request):
    
    item_filter = rosine( request, Bordereau , BordereauFilter , 'req_bordereau' )

    return render(request,'bordereau/list.html',{ 'bordereau_pages':'active' , 'items': item_filter  } )

@permission_required('archivages_app.add_scan', login_url='colis_apps:denied')
def add_bordereau(request):
    
    return ajout_de_scans(request, BordereauForm, ScanFichierForm, ScanFichier , 'bordereau')

@permission_required('archivages_app.view_scan', login_url='colis_apps:denied')
def update_bordereau(request, _id ):
    
    return mise_a_jour_scans( request, _id, Bordereau, ScanFichier, BordereauForm, ScanFichierForm, 'archivages_app.change_scan', 'observation', 'bordereau')

@permission_required('archivages_app.delete_scan', login_url='colis_apps:denied')
def delete_bordereau(request, _id ):
    item = Bordereau.objects.get( pk = _id )
    item.delete()
    messages.success( request,('Item has been deleted') )
    return redirect('archivages_app:list.bordereau')

@permission_required('archivages_app.delete_scan', login_url='colis_apps:denied')
def delete_file_bordereau(request, file_id , _id ):
    item = ScanFichier.objects.get( pk = file_id )
    item.delete()
    messages.success( request,'File has been deleted')
    return redirect('archivages_app:update.bordereau' , _id )

#---------------------------------------------------------------------------------------#

@permission_required('archivages_app.view_scan', login_url='colis_apps:denied')
def list_bleue(request):

    item_filter = rosine(request,Bleue,BleueFilter,'req_bleue')

    return render(request,'bleue/list.html',{ 'items': item_filter  } )

@permission_required('archivages_app.add_scan', login_url='colis_apps:denied')
def add_bleue(request):

    return ajout_de_scans( request , BleueForm , ScanFichierForm , ScanFichier , 'bleue')

@permission_required('archivages_app.view_scan', login_url='colis_apps:denied')
def update_bleue(request, _id ):
    
    return mise_a_jour_scans( request, _id, Bleue, ScanFichier, BleueForm, ScanFichierForm, 'archivages_app.change_scan', 'observation', 'bleue')

@permission_required('archivages_app.delete_scan', login_url='colis_apps:denied')
def delete_bleue(request, _id ):
    item = Bleue.objects.get( pk = _id )
    item.delete()
    messages.success( request,('Item has been deleted') )
    return redirect('archivages_app:list.bleue')

@permission_required('archivages_app.delete_scan', login_url='colis_apps:denied')
def delete_file_bleue(request, file_id , _id ):
    item = ScanFichier.objects.get( pk = file_id )
    item.delete()
    messages.success( request,'File has been deleted')
    return redirect('archivages_app:update.bleue' , _id )

#----------------------------------------------------------------------------------------#

@permission_required('archivages_app.view_scan', login_url='colis_apps:denied')
def list_assurance(request):

    item_filter = rosine( request, Assurance , AssuranceFilter , 'req_assurance')

    return render( request,'assurance/list.html',{'items': item_filter } )

@permission_required('archivages_app.add_scan', login_url='colis_apps:denied')
def add_assurance(request) :

    return ajout_de_scans( request, AssuranceForm , ScanFichierForm, ScanFichier, 'assurance')

@permission_required('archivages_app.view_scan', login_url='colis_apps:denied')
def update_assurance(request, _id):

    return mise_a_jour_scans( request , _id , Assurance , ScanFichier , AssuranceForm, ScanFichierForm , 'archivages_app.change_scan','observation', 'assurance')

@permission_required('archivages_app.delete_scan', login_url='colis_apps:denied')
def delete_assurance( request , _id ):

    return suppression_scan ( request , _id , Assurance , 'assurance')

@permission_required('archivages_app.delete_scan', login_url='colis_apps:denied')
def delete_file_assurance( request , file_id , _id ):

    return suppression_scan_fichier ( request , file_id , _id , ScanFichier , 'assurance')


#-----------------------------------------------------------------------------------------#

@permission_required('archivages_app.view_scan', login_url='colis_apps:denied')
def list_plainte(request):

    item_filter = rosine( request , Plainte , PlainteFilter , 'req_plainte')

    return render( request,'plainte/list.html',{'items': item_filter } )

@permission_required('archivages_app.add_scan', login_url='colis_apps:denied')
def add_plainte(request):
    return ajout_de_scans( request , PlainteForm , ScanFichierForm , ScanFichier , 'plainte')

@permission_required('archivages_app.view_scan', login_url='colis_apps:denied')
def update_plainte(request, _id):
    return mise_a_jour_scans( request , _id, Plainte , ScanFichier, PlainteForm, ScanFichierForm, 'archivages_app.change_scan', 'observation', 'plainte')

@permission_required('archivages_app.delete_scan', login_url='colis_apps:denied')
def delete_plainte( request , _id ):
    return suppression_scan ( request, _id, Plainte , 'plainte')

@permission_required('archivages_app.delete_scan', login_url='colis_apps:denied')
def delete_file_plainte ( request , file_id , _id ):
    return suppression_scan_fichier ( request , file_id, _id, ScanFichier , 'plainte')