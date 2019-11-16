import django_filters
from .models import Coli
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
#from bootstrap_datepicker.widgets import DatePicker
from bootstrap_datepicker_plus import DateTimePickerInput , DatePickerInput , TimePickerInput
from django.db import models
from django import forms
from django_filters.widgets import RangeWidget

class ColiFilter(django_filters.FilterSet):

    date_lte = django_filters.DateFilter(field_name='dateheure', 
    lookup_expr='gte' , 
    label='Date debut' , 
    widget= DatePicker( options={'format': 'MM/D/YYYY'}, attrs={'append': 'fa fa-calendar',} ) )
    
    date_gte = django_filters.DateFilter(field_name='dateheure', 
    lookup_expr='lte' , 
    label='Date fin' , 
    widget= DatePicker( options={'format': 'MM/D/YYYY'}, attrs={'append': 'fa fa-calendar',} ) )
    
    #time_lte = django_filters.TimeFilter(field_name='dateheure', 
    #lookup_expr='time__gte' , 
    #label='Heure debut' , 
    #widget= TimePicker( options={'format': 'HH:mm'}, attrs={'append': 'fa fa-clock',} ) )
    
    #time_gte = django_filters.TimeFilter(field_name='dateheure', 
    #lookup_expr='time__lte' , 
    #label='Heure fin' , 
    #widget= TimePicker( options={'format': 'HH:mm'}, attrs={'append': 'fa fa-clock',} ) )
    
    #datetime = django_filters.DateTimeFromToRangeFilter( widget=RangeWidget(attrs={'type': DateTimePickerInput() }) )
    numero_colis = django_filters.CharFilter(label='Colis ID', lookup_expr='icontains')
    telephone_exp = django_filters.CharFilter(label='Tel. Exp.', lookup_expr='icontains')
    telephone_dest = django_filters.CharFilter(label='Tel. Dest.', lookup_expr='icontains')
    immatriculation__immatriculation = django_filters.CharFilter( label='Imm.', lookup_expr='icontains')

    class Meta :
        model = Coli
        fields = ['numero_colis', 'telephone_exp' , 'immatriculation','etat_colis','destination']
        filter_overrides = {
            models.DateTimeField : {
                'filter_class': django_filters.DateTimeFilter,
                'extra': lambda f : {
                    'widget': DateTimePickerInput(),
                },
            },
        }

