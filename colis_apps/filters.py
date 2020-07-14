import django_filters
from .models import Coli , Client
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
from django.db import models
from django import forms
import datetime

class ColiFilter(django_filters.FilterSet):

    date_lte = django_filters.DateTimeFilter(field_name='dateheure', 
    lookup_expr='gte' , 
    label='Date debut' , 
    widget= DateTimePicker( 
        options={'format': 'MM/D/YYYY HH:mm' , "icons": {"time": "fa fa-clock"} }, 
        attrs={'append': 'fa fa-calendar',} ) )
    
    date_gte = django_filters.DateTimeFilter(field_name='dateheure', 
    lookup_expr='lte' , 
    label='Date fin' , 
    widget= DateTimePicker( 
        options={'format': 'MM/D/YYYY HH:mm', "icons": {"time": "fa fa-clock"} }, 
        attrs={'append': 'fa fa-calendar',} ) )
    
    numero_colis = django_filters.CharFilter(label='Colis ID', lookup_expr='icontains')
    telephone_exp__phone = django_filters.CharFilter(label='Tel. Exp.', lookup_expr='icontains')
    telephone_dest__phone = django_filters.CharFilter(label='Tel. Dest.', lookup_expr='icontains')
    immatriculation__immatriculation = django_filters.CharFilter(  label='Imm.', lookup_expr='icontains')

    class Meta :
        model = Coli
        fields = ['numero_colis', 'telephone_exp' , 'telephone_dest','etat_colis','destination']

class ClientFilter(django_filters.FilterSet):

    date_lte = django_filters.DateTimeFilter(field_name='client_created_at', 
    lookup_expr='gte' , 
    label='Date debut' , 
    widget= DateTimePicker( 
        options={'format': 'MM/D/YYYY HH:mm'}, 
        attrs={'append': 'fa fa-calendar',} ) )
    
    date_gte = django_filters.DateTimeFilter(field_name='client_created_at', 
    lookup_expr='lte' , 
    label='Date fin' , 
    widget= DateTimePicker( 
        options={'format': 'MM/D/YYYY HH:mm'}, 
        attrs={'append': 'fa fa-calendar',} ) )

    phone = django_filters.CharFilter(label='Telephone', lookup_expr='icontains')
    nom = django_filters.CharFilter(label='Nom', lookup_expr='icontains')

    class Meta :
        model = Client
        fields = ['phone', 'nom']
