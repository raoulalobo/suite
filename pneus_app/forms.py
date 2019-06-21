from django import forms
from .models import Pneu
from django.forms import ClearableFileInput
from bootstrap_datepicker_plus import DateTimePickerInput


class PneuForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Pneu
        fields = ('date', 'immatriculation', 'kilometrage','marque_pneu','nbr_pneu','responsable' , 'chauffeur' , 'observation' )
        widgets = {
            'date': DateTimePickerInput(), # default date-format %m/%d/%Y will be used
        }
