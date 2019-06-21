from django import forms
from .models import Plainte , PlainteFile
from django.forms import ClearableFileInput
from bootstrap_datepicker_plus import DateTimePickerInput


class PlainteForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Plainte
        fields = ('dateheure', 'ville_plainte', 'raison_plainte','etat_plainte','plaignant','telephone_p' , 'detail_plainte' , 'numero_colis', 'immatriculation', 'resolution_observation')
        widgets = {
            'dateheure': DateTimePickerInput(), # default date-format %m/%d/%Y will be used
        }


class FileModelForm(forms.ModelForm):
    class Meta:
        model = PlainteFile
        fields = ('file',)
        widgets = {
            'file': ClearableFileInput(attrs={'multiple': True}),
        }