import django_filters
from .models import Car, Pneu
from bootstrap_datepicker_plus import DateTimePickerInput
from django.db import models
from django import forms

class PneuFilter(django_filters.FilterSet):

    date_lte = django_filters.DateTimeFilter(field_name='date', lookup_expr='date__gte' , label='Date debut' , widget= DateTimePickerInput() )
    date_gte = django_filters.DateTimeFilter(field_name='date', lookup_expr='date__lte' , label='Date fin' , widget= DateTimePickerInput() )
    marque_pneu = django_filters.CharFilter(label='Marque', lookup_expr='icontains')

    class Meta :
        model = Pneu
        fields = ['immatriculation', 'marque_pneu']
        filter_overrides = {
            models.DateTimeField : {
                'filter_class': django_filters.DateTimeFilter,
                'extra': lambda f : {
                    'widget': DateTimePickerInput(),
                },
            },
        }

