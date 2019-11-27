import django_filters
from .models import Scan, Facture, Bordereau , Bleue,  Assurance , Plainte , Explication
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
#from bootstrap_datepicker.widgets import DatePicker
from bootstrap_datepicker_plus import DateTimePickerInput , DatePickerInput , TimePickerInput
from django.db import models
from django import forms
from django_filters.widgets import RangeWidget


class ScanFilter(django_filters.FilterSet):

    date_lte = django_filters.DateFilter(field_name='date', 
    lookup_expr='gte' , 
    label='Date debut' , 
    widget= DatePicker( options={'format': 'MM/D/YYYY'}, attrs={'append': 'fa fa-calendar',} ) )
    
    date_gte = django_filters.DateFilter(field_name='date', 
    lookup_expr='lte' , 
    label='Date fin' , 
    widget= DatePicker( options={'format': 'MM/D/YYYY'}, attrs={'append': 'fa fa-calendar',} ) )
    
    ville = django_filters.CharFilter(label='Ville', lookup_expr='icontains')
    cars__immatriculation = django_filters.CharFilter( label='Imm.', lookup_expr='icontains')

    class Meta :
        model = Scan
        fields = ( 'date', 'ville', 'cars' )
        filter_overrides = {
            models.DateTimeField : {
                'filter_class': django_filters.DateTimeFilter,
                'extra': lambda f : {
                    'widget': DateTimePickerInput(),
                },
            },
        }


class FactureFilter(ScanFilter):

    demandeur = django_filters.CharFilter(label='Demandeur', lookup_expr='icontains')
    caissier = django_filters.CharFilter(label='Caissier', lookup_expr='icontains')
    categorie__categories = django_filters.CharFilter( label='Categorie', lookup_expr='icontains')

    class Meta(ScanFilter.Meta) :
        model = Facture
        fields = ScanFilter.Meta.fields + ('demandeur','caissier', 'categorie' )
        exclude = ('ville',)

class BordereauFilter(ScanFilter):

    class Meta(ScanFilter.Meta) :
        model = Bordereau


class BleueFilter(ScanFilter):

    numero_bleue = django_filters.CharFilter(label='#Bleue', lookup_expr='icontains')
  
    class Meta(ScanFilter.Meta) :
        model = Bleue
        fields = ScanFilter.Meta.fields + ('numero_bleue', )
        exclude = ('ville',)


class AssuranceFilter(ScanFilter):

    numero_assurance = django_filters.CharFilter(label='#Assurance', lookup_expr='icontains')
  
    class Meta(ScanFilter.Meta) :
        model = Assurance
        fields = ScanFilter.Meta.fields + ('numero_assurance', )
        exclude = ('ville',)

class PlainteFilter(ScanFilter):

    phone = django_filters.CharFilter(label='#Telephone', lookup_expr='icontains')
  
    class Meta(ScanFilter.Meta) :
        model = Plainte
        fields = ScanFilter.Meta.fields + ('phone', )
        exclude = ('ville',)


class ExplicationFilter(ScanFilter):

    nom = django_filters.CharFilter(label='Nom', lookup_expr='icontains')
  
    class Meta(ScanFilter.Meta) :
        model = Explication
        fields = ScanFilter.Meta.fields + ('nom', 'reponse' )
        exclude = ('ville','cars')

