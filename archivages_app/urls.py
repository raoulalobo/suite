from django.urls import path
from . import views


app_name = 'archivages_app'
urlpatterns = [

    # URL access denied

    # URL scan Facture models
    #path('accces-denied/', views.denied, name='denied'),
    #path('detail/<coli_id>', views.detail_coli, name='detail.coli'),
    #path('delete/<coli_id>', views.delete, name='delete'),
    #path('rapport/', views.rapport_coli, name='rapport.coli'),
    path('list/facture', views.list_facture, name='list.facture'),
    path('add/facture', views.add_facture, name='add.facture'),
    path('update/facture/<_id>', views.update_facture, name='update.facture'),
    path('delete/facture/<_id>', views.delete_facture, name='delete.facture'),
    path('delete/facture/<file_id>/<_id>', views.delete_file_facture, name='delete.file.facture'),


    path('list/bordereau', views.list_bordereau, name='list.bordereau'),
    path('add/bordereau', views.add_bordereau, name='add.bordereau'),
    path('update/bordereau/<_id>', views.update_bordereau, name='update.bordereau'),
    path('delete/bordereau/<_id>', views.delete_bordereau, name='delete.bordereau'),
    path('delete/bordereau/<file_id>/<_id>', views.delete_file_bordereau, name='delete.file.bordereau'),


    path('list/bleue', views.list_bleue, name='list.bleue'),
    path('add/bleue', views.add_bleue, name='add.bleue'),
    path('update/bleue/<_id>', views.update_bleue, name='update.bleue'),
    path('delete/bleue/<_id>', views.delete_bleue, name='delete.bleue'),
    path('delete/bleue/<file_id>/<_id>', views.delete_file_bleue, name='delete.file.bleue'),


    path('list/assurance', views.list_assurance, name='list.assurance'),
    path('add/assurance', views.add_assurance, name='add.assurance'),
    path('update/assurance/<_id>', views.update_assurance, name='update.assurance'),
    path('delete/assurance/<_id>', views.delete_assurance, name='delete.assurance'),
    path('delete/assurance/<file_id>/<_id>', views.delete_file_assurance, name='delete.file.assurance'),


    path('list/plainte', views.list_plainte, name='list.plainte'),
    path('add/plainte', views.add_plainte, name='add.plainte'),
    path('update/plainte/<_id>', views.update_plainte, name='update.plainte'),
    path('delete/plainte/<_id>', views.delete_plainte, name='delete.plainte'),
    path('delete/plainte/<file_id>/<_id>', views.delete_file_plainte, name='delete.file.plainte'),


]