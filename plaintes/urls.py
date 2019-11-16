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
from django.urls import path, include

# imports pour fichiers ( Images , Word ).
from django.conf import settings
from django.conf.urls.static import static
from .fct import one_time_startup

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    #path('plaintes/', include('plaintes_app.urls', namespace='plaintes')),
    path('archivages/', include('archivages_app.urls', namespace='archivages')),
    path('pneus/', include('pneus_app.urls', namespace='pneus')),
    path('mtickets/', include('mtickets_apps.urls', namespace='mtickets')),
    path('', include('colis_apps.urls', namespace='colis')),
    path('account/', include('account.urls', namespace='account')),
]

one_time_startup()

# Pourquoi cette ligne permet l'affichage des images.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)

