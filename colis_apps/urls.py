from django.urls import path
from django.conf.urls import url
from . import views


app_name = 'colis_apps'
urlpatterns = [

    # URL
    path('', views.homeredirect, name='homeredirect'),
    path('accces-denied/', views.denied, name='denied'),
    path('list/coli', views.list_coli, name='list.coli'),
    path('rapport/', views.rapport_coli, name='rapport.coli'),
    path('add/', views.add_coli, name='add.coli'),
    path('update/<coli_id>', views.update_coli, name='update.coli'),
    path('detail/<coli_id>', views.detail_coli, name='detail.coli'),
    path('delete/<coli_id>', views.delete, name='delete'),
    path('delete/coli/<coli_id>', views.delete_coli, name='delete.coli'),
    path('delete/<file_id>/<coli_id>', views.delete_file, name='delete.file'),
]