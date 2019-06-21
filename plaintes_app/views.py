from django.shortcuts import render , redirect
from .forms import PlainteForm , FileModelForm
from .models import Plainte, PlainteFile
from django.contrib import messages

# Create your views here.


def list_plaintes(request):

    plaintes = Plainte.objects.all()
    
    return render(request,'list.html',{ 'plaintes': plaintes })


def add_plainte(request):
    if request.method == 'POST':
        plainte_form = PlainteForm(request.POST )
        file_form = FileModelForm( request.POST , request.FILES )
        files = request.FILES.getlist('file') 
        if plainte_form.is_valid() and file_form.is_valid() :
            plainte = plainte_form.save()
            for f in files :
                file_instance = PlainteFile(file=f, plainte=plainte )
                file_instance.save()
            return redirect('plaintes:list.plaintes')
    else:
        plainte_form = PlainteForm()
        file_form = FileModelForm()

    return render(request,'add.html',{'plainte_form': plainte_form , 'file_form' : file_form })

def update_plainte(request, plainte_id ):
    item = Plainte.objects.get( pk = plainte_id )
    joint = PlainteFile.objects.filter( plainte_id = plainte_id )
    plainte_form = PlainteForm(request.POST or None, instance=item )
    file_form = FileModelForm( request.POST or None , request.FILES  )
    files = request.FILES.getlist('file')
    if plainte_form.is_valid() and file_form.is_valid() :
        plainte = plainte_form.save()
        for f in files :
                file_instance = PlainteFile(file=f, plainte=plainte )
                file_instance.save()
        return redirect('plaintes:list.plaintes')
    else:
        plainte_form = PlainteForm( None,  instance=item )
        file_form = FileModelForm()

    return render(request, 'add.html', { 'plainte_form': plainte_form , 'file_form' : file_form , 'joint': joint })


def detail_plainte(request, plainte_id ):
    
    item = Plainte.objects.get( pk = plainte_id )
    files = PlainteFile.objects.filter(plainte_id = plainte_id )

    return render(request,'detail.html',{'item': item , 'files': files })


def delete_plainte(request, plainte_id ):
    item = Plainte.objects.get( pk = plainte_id )
    item.delete()
    #messages.succes( request,('Item has been deleted') )
    return redirect('plaintes:list.plaintes')

def delete_file(request, file_id , plainte_id ):
    item = PlainteFile.objects.get( pk = file_id )
    item.delete()
    messages.success( request,'Item has been deleted')
    return redirect('plaintes:update.plainte' , plainte_id )