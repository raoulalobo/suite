#https://docs.djangoproject.com/fr/2.2/topics/forms/modelforms/

from django import forms
from .models import Scan, Facture, Bordereau, Bleue, Assurance, ScanFichier, Plainte, Explication
from django.forms import ClearableFileInput , Textarea
#from bootstrap_datepicker_plus import DateTimePickerInput
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
from django.utils.translation import gettext_lazy as _


class ScanForm(forms.ModelForm):

    class Meta:
        model = Scan
        fields = ( 'date', 'ville', 'cars', 'libelle' )
        labels = {
            'date': _('Date'),
        }
        help_texts = {
            'date': _('Entrez la date'),
        }
        widgets = {
            'date': DatePicker(
                options={'format': 'MM/D/YYYY'},
                attrs={'append': 'fa fa-calendar',}
            )
        }


class FactureForm(ScanForm):

    class Meta(ScanForm.Meta):
        model = Facture
        fields = ScanForm.Meta.fields +('demandeur','caissier','montant','categorie' , 'observation')
        labels = {
            'date': _('Date de paiement'),
        }

#-----------------------------------------------------------------------------------------#

class BordereauForm(ScanForm):

    class Meta(ScanForm.Meta):
        model = Bordereau
        fields = ScanForm.Meta.fields + ('observation' ,)
        labels = {
            'date': ('Date de voyage'),
        }

#----------------------------------------------------------------------------------------#

class BleueForm(ScanForm):

    class Meta(ScanForm.Meta):
        model = Bleue
        fields = ScanForm.Meta.fields + ('numero_bleue','observation' )
        labels = {
            'date': _('Date expiration'),
        }

#----------------------------------------------------------------------------------------#

class AssuranceForm(ScanForm):

    class Meta(ScanForm.Meta):
        model = Assurance
        fields = ScanForm.Meta.fields + ('numero_assurance','observation' )
        labels = {
            'libelle': _('Assureur'),
        }

#----------------------------------------------------------------------------------------#

class PlainteForm(ScanForm):

    class Meta(ScanForm.Meta):
        model = Plainte
        fields = ScanForm.Meta.fields + ('plaignant','phone','status','observation' )


#----------------------------------------------------------------------------------------#

class ExplicationForm(ScanForm):

    class Meta(ScanForm.Meta):
        model = Explication
        fields = ScanForm.Meta.fields + ('nom','poste','reponse','observation' )
        labels = {
            'libelle': _('Objet'),
        }


#----------------------------------------------------------------------------------------#


class ScanFichierForm(forms.ModelForm):
    class Meta:
        model = ScanFichier
        fields = ('file',)
        widgets = {
            'file': ClearableFileInput(attrs={'multiple': True}),
        }
