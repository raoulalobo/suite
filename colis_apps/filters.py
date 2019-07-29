import django_filters
from .models import Coli
from bootstrap_datepicker_plus import DateTimePickerInput , DatePickerInput , TimePickerInput
from django.db import models
from django import forms
from django_filters.widgets import RangeWidget

class ColiFilter(django_filters.FilterSet):

    date_lte = django_filters.DateFilter(field_name='dateheure', lookup_expr='date__gte' , label='Date debut' , widget= DatePickerInput() )
    date_gte = django_filters.DateFilter(field_name='dateheure', lookup_expr='date__lte' , label='Date fin' , widget= DatePickerInput() )
    time_lte = django_filters.TimeFilter(field_name='dateheure', lookup_expr='time__gte' , label='Heure debut' , widget= TimePickerInput() )
    time_gte = django_filters.TimeFilter(field_name='dateheure', lookup_expr='time__lte' , label='Heure fin' , widget= TimePickerInput() )
    #dateheure = django_filters.DateTimeFromToRangeFilter(widget=RangeWidget(attrs={'type': 'date'}))
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

