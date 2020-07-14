"""plaintes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url

# imports pour fichiers ( Images , Word ).
from django.conf import settings
from django.conf.urls.static import static

#import de la fonction one_time_startup
from .fct import one_time_startup

from colis_apps.views import CountryAutocomplete , ClientNomAutocomplete , ClientPhoneAutocomplete
from archivages_app.views import CarAutocomplete
admin.autodiscover()

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    #re_path(r'^select2/', include('django_select2.urls')),
    #path('plaintes/', include('plaintes_app.urls', namespace='plaintes')),
    path('archivages/', include('archivages_app.urls', namespace='archivages')),
    path('pneus/', include('pneus_app.urls', namespace='pneus')),
    path('mtickets/', include('mtickets_apps.urls', namespace='mtickets')),
    path('', include('colis_apps.urls', namespace='colis')),
    path('account/', include('account.urls', namespace='account')),
    url(r'^select2/', include('django_select2.urls')),
    url(r'^client-phone-autocomplete/$',ClientPhoneAutocomplete.as_view(),name='client-phone-autocomplete',),
    url(r'^client-nom-autocomplete/$',ClientNomAutocomplete.as_view(create_field='nom'),name='client-nom-autocomplete',),
    url(r'^country-autocomplete/$',CountryAutocomplete.as_view(),name='country-autocomplete',),
    url(r'^car-autocomplete/$',CarAutocomplete.as_view(),name='car-autocomplete',),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# Vient du fichier Views de Colis 
one_time_startup()

# Pourquoi cette ligne permet l'affichage des images.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    

