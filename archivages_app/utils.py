import datetime
from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render
import random
import string

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def rosine( request, modele, le_filtre, sess ) :
    
    itemss = modele.objects.all()
    items = modele.objects.all().filter( date__gte = datetime.date.today() )

    req_item = request.GET
    req_item_list_key = list(req_item.keys())
    req_item_list_value = list(req_item.values())
    req_item_list_len = len(req_item_list_key)

    
    if req_item_list_key :
    #Si les keys values existent ca veut dire q on clique sur la recherche    

        if not (  bool( req_item_list_value[1] ) and bool( req_item_list_value[2] ) ):
        #Si les champs dates sont vides filtrer les donnees sur la date du jour
            item_filter = le_filtre( request.GET , queryset= items )
        else:  
            item_filter = le_filtre( request.GET , queryset= itemss )
        #    
        request.session[sess] = request.GET

        
    if not req_item_list_key and ( sess not in request.session ):
    #Si les keys values existent pas te q il ya pas de session req_pneu filter sur la date du jour
    #Cas utilisation : retour vers la liste principale suite a un ajout, modification ou sppression apres recherche
        item_filter = le_filtre( request.GET , queryset= items )
    else :
    #Cas utilisation : Retour vers la liste principale suite a un ajout , modification ou suppression apres recherche    
        item_filter = le_filtre( request.session[sess] , queryset= itemss )

 
    return item_filter

def ajout_de_scans( request ,formulaire, formulaire_scan ,  modele_scan, dossier  ):

    if request.method == 'POST':
        form = formulaire(request.POST )
        file_form = formulaire_scan( request.POST , request.FILES )
        files = request.FILES.getlist('file') 
        if form.is_valid() and file_form.is_valid() :
            facture = form.save()
            for f in files :
                #ajouter un tache avec celery ici
                file_instance = modele_scan( file=f, scanfichier=facture )
                file_instance.save()

            messages.success( request,'Item has been added')
            #return redirect(redirection)
            return redirect('archivages_app:list.{}'.format( dossier )) 
    else:
        form = formulaire()
        file_form = formulaire_scan()

    #return form , file_form
    return render(request,'{}/add.html'.format( dossier ),{'form': form , 'file_form' : file_form , 'titre' : dossier })

def mise_a_jour_scans( request, _id , modele , modele_scan , formulaire , formulaire_scan, droits , champs_a_modifier, dossier ) :
    
    #Requetes sur modeles
    item = modele.objects.get( pk = _id )
    joint = modele_scan.objects.filter( scanfichier = _id )
    history = modele.history.filter( id = _id )
    #Formulaires
    form = formulaire(request.POST or None, instance= item )
    file_form = formulaire_scan( request.POST or None , request.FILES  )
    files = request.FILES.getlist('file')
    

    if form.is_valid() and file_form.is_valid() :
        commit = form.save(commit=False)

        #if request.user.has_perm('colis_apps.delete_coli'):
        if request.user.has_perm(droits):
            facture = commit.save()
        else:
            facture = commit.save(update_fields=[champs_a_modifier])

        for f in files :
            file_instance = modele_scan(file=f, scanfichier= commit )
            file_instance.save() 
       
            
        messages.success( request,'Item has been updated')
        return redirect('archivages_app:list.{}'.format( dossier))
    else:
        form = formulaire( None,  instance=item )
        file_form = formulaire_scan()


    return render(request, '{}/add.html'.format( dossier), { 'form': form , 'file_form' : file_form , 'joint': joint , 'history': history, 'item': item, 'update': True , 'titre': dossier })

    #return  form , file_form , joint , history , item 

def suppression_scan( request , _id , modele , dossier ) :

    item = modele.objects.get( pk = _id )
    item.delete()
    messages.success( request,('Item has been deleted') )
    return redirect('archivages_app:list.{}'.format( dossier ))


def suppression_scan_fichier( request , file_id , _id , modele_scan , dossier ):

    item = modele_scan.objects.get( pk = file_id )
    item.delete()
    messages.success( request,'File has been deleted')
    return redirect('archivages_app:update.{}'.format( dossier ) , _id )