from django.urls import path
from . import views


app_name = 'pneus_app'
urlpatterns = [

    #URL
    path('list/', views.list_pneus, name='list.pneu'),
    path('add/', views.add_pneu, name='add.pneu'),
    path('detail/<pneu_id>', views.detail_pneu, name='detail.pneu'),
    path('update/<pneu_id>', views.update_pneu, name='update.pneu'),
    path('export/', views.export, name='export.pneu'),
    #path('delete/<plainte_id>', views.delete_plainte, name='delete.plainte'),
    #path('delete/<file_id>/<plainte_id>', views.delete_file, name='delete.file'),
]