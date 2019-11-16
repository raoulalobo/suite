from django.urls import path
from . import views


app_name = 'mtickets_apps'
urlpatterns = [

    # URL
    #path('accces-denied/', views.denied, name='denied'),
    path('list', views.list_mtickets, name='list.mtickets'),
    #path('rapport/', views.rapport_coli, name='rapport.coli'),
    path('add/', views.add_mticket, name='add.mticket'),
    path('update/<_id>', views.update_mticket, name='update.mticket'),
    path('detail/<mticket_id>', views.detail_mticket, name='detail.mticket'),
    path('delete/<mticket_id>', views.delete, name='delete.mticket'),
    path('delete/coli/<mticket_id>', views.delete_mticket, name='deleted.mticket'),
    #path('delete/<file_id>/<coli_id>', views.delete_file, name='delete.file'),
]