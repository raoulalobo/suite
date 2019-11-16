#https://docs.djangoproject.com/fr/2.2/topics/forms/modelforms/

from django import forms
from .models import Facture, Bordereau, Bleue, Assurance, ScanFichier
from django.forms import ClearableFileInput , Textarea
#from bootstrap_datepicker_plus import DateTimePickerInput
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
from django.utils.translation import gettext_lazy as _

class FactureForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super( FactureForm, self ).__init__(*args, **kwargs)
        #https://docs.djangoproject.com/fr/2.2/ref/forms/widgets/
        self.fields['cars'].widget.attrs.update({'class': 'special'})


    class Meta:

        model = Facture
        fields = ('date', 'ville','cars','libelle','demandeur','caissier','montant','observation' )
        labels = {
            'date': _('Date de paiement'),
        }
        help_texts = {
            'date': _('Entrez la date et heure'),
        }
        widgets = {
            'date': DatePicker(
                options={'format': 'MM/D/YYYY'},
                attrs={'append': 'fa fa-calendar',}
            )
            #'numero_colis': Textarea(attrs={'cols': 80, 'rows': 20, 'readonly': True}),
            #'dateheure': DateTimePickerInput(), # default date-format %m/%d/%Y will be used
        }



class ScanFichierForm(forms.ModelForm):
    class Meta:
        model = ScanFichier
        fields = ('file',)
        widgets = {
            'file': ClearableFileInput(attrs={'multiple': True}),
        }


#-----------------------------------------------------------------------------------------#


class BordereauForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super( BordereauForm, self ).__init__(*args, **kwargs)
        self.fields['cars'].widget.attrs.update({'class': 'special'})


    class Meta:

        model = Bordereau
        fields = ('date', 'ville','cars','libelle','observation' )
        labels = {
            'date': ('Date de voyage'),
        }
        help_texts = {
            'date': ('Entrez la date et heure'),
        }
        widgets = {
            'date': DatePicker(
                options={'format': 'MM/D/YYYY'},
                attrs={'append': 'fa fa-calendar',}
            )
        }



#----------------------------------------------------------------------------------------#

class BleueForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super( BleueForm, self ).__init__(*args, **kwargs)

    class Meta:

        model = Bleue
        fields = ('cars', 'numero_bleue','observation' )
