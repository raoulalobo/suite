from django import forms
from .models import Coli , ColisFile
from django.forms import ClearableFileInput , Textarea
from bootstrap_datepicker_plus import DateTimePickerInput


class ColiForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super( ColiForm, self ).__init__(*args, **kwargs)


    class Meta:
        model = Coli
        fields = ('numero_colis', 'nom_exp', 'telephone_exp', 'nom_dest', 'telephone_dest','immatriculation','destination','valeur_declaree','montant' , 'libelle' , 'etat_colis', 'emplacement', 'observation' )
        widgets = {
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