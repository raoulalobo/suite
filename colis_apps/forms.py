from django import forms
from .models import Coli , ColisFile ,Client
from cars_app.models import Car
from django.forms import ClearableFileInput , Textarea, TextInput, ChoiceField
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
import re

from dal import autocomplete , forward


from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_5(value):
    if value % 5 != 0:
        raise ValidationError(
            _('<<%(value)s>> est 01 format invalide'),
            params={'value': value},
        )


class ClientForm(forms.ModelForm):
    
    class Meta :
        model = Client

        fields = ('phone', 'nom', 'cni', 'birthday', 'ville', 'quartier') 
        labels = {
            'birthday': _('Date de naissance'),
        }
        widgets = {
            'birthday': DatePicker(
                options={'format': 'MM/D/YYYY'},
                attrs={'append': 'fa fa-calendar',}
            )
        } 

class ColiForm(forms.ModelForm):

    immatriculation = forms.ModelChoiceField( queryset=Car.objects.all(),widget=autocomplete.ModelSelect2(url='country-autocomplete'))
    telephone_exp = forms.ModelChoiceField( queryset=Client.objects.all(), widget=autocomplete.ModelSelect2(url='client-phone-autocomplete'))
    #nom_exp = forms.ModelChoiceField( queryset=Client.objects.all(),widget=autocomplete.ModelSelect2(url='client-nom-autocomplete', forward=(forward.Field('telephone_exp', 'id'),) ))
    telephone_dest = forms.ModelChoiceField( queryset=Client.objects.all(), widget=autocomplete.ModelSelect2(url='client-phone-autocomplete'))
    #nom_dest = forms.ModelChoiceField( queryset=Client.objects.all(),widget=autocomplete.ModelSelect2(url='client-nom-autocomplete', forward=(forward.Field('telephone_dest', 'id'),) ))
    montant = forms.IntegerField(validators=[validate_5]) # Ceci annule ce que il y a sous Meta


    class Meta:
        model = Coli
        
        fields = ('telephone_exp', 'telephone_dest', 'immatriculation','destination','valeur_declaree','montant' , 'libelle' , 'etat_colis', 'emplacement', 'observation' )
        labels = {
            'montant':_('Money'),
        }
        help_texts = {
            #'telephone_exp': _('Exemple : 699999999-John Doe'),
        }
        widgets = {
            #'libelle': MyWidget()
            #'libelle': autocomplete.ModelSelect2(url='country-autocomplete')
            #'immatriculation': AutoCompleteSelectMultipleField('cars', required=False, help_text=None)
            #'numero_colis': Textarea(attrs={'cols': 80, 'rows': 20, 'readonly': True}),
            #'dateheure': DateTimePickerInput(), # default date-format %m/%d/%Y will be used
        }


class ColiFileForm(forms.ModelForm):
    class Meta:
        model = ColisFile
        fields = ('file',)
        widgets = {
            'file': ClearableFileInput(attrs={'multiple': True}),
        }