import django_filters
from .models import Mticket
from bootstrap_datepicker_plus import DateTimePickerInput , DatePickerInput , TimePickerInput
from django.db import models
from django import forms
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
from django_filters.widgets import RangeWidget

class MticketFilter(django_filters.FilterSet):

    date_lte = django_filters.DateFilter(field_name='dateheure', 
    lookup_expr='gte' , 
    label='Date debut' , 
    widget= DatePicker( options={'format': 'MM/D/YYYY'}, attrs={'append': 'fa fa-calendar',} ) )
    date_gte = django_filters.DateFilter(field_name='dateheure', 
    lookup_expr='lte' , 
    label='Date fin' , 
    widget= DatePicker( options={'format': 'MM/D/YYYY'}, attrs={'append': 'fa fa-calendar',} ) )
    name = django_filters.CharFilter(label='Nom', lookup_expr='icontains')
    cni = django_filters.CharFilter(label='CNI', lookup_expr='icontains')
    ticket = django_filters.CharFilter(label='Mticket', lookup_expr='icontains')
    partner__partenaire = django_filters.CharFilter( label='startUp', lookup_expr='icontains')

    class Meta :
        model = Mticket
        fields = ['name', 'cni' , 'ticket','partner']
        filter_overrides = {
            models.DateTimeField : {
                'filter_class': django_filters.DateTimeFilter,
                'extra': lambda f : {
                    'widget': DateTimePickerInput(),
                },
            },
        }

