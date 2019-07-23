import django_filters
from .models import Coli
from bootstrap_datepicker_plus import DateTimePickerInput
from django.db import models
from django import forms

class ColiFilter(django_filters.FilterSet):

    date_lte = django_filters.DateTimeFilter(field_name='dateheure', lookup_expr='date__gte' , label='Date debut' , widget= DateTimePickerInput() )
    date_gte = django_filters.DateTimeFilter(field_name='dateheure', lookup_expr='date__lte' , label='Date fin' , widget= DateTimePickerInput() )
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

