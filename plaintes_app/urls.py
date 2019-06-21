from django.urls import path
from . import views


app_name = 'plaintes_app'
urlpatterns = [

    # URL
    path('list/', views.list_plaintes, name='list.plaintes'),
    path('add/', views.add_plainte, name='add.plainte'),
    path('detail/<plainte_id>', views.detail_plainte, name='detail.plainte'),
    path('update/<plainte_id>', views.update_plainte, name='update.plainte'),
    path('delete/<plainte_id>', views.delete_plainte, name='delete.plainte'),
    path('delete/<file_id>/<plainte_id>', views.delete_file, name='delete.file'),
]