from django import forms
from .models import Mticket , Partner
from django.forms import ClearableFileInput , Textarea
from bootstrap_datepicker_plus import DateTimePickerInput


class MticketForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super( MticketForm, self ).__init__(*args, **kwargs)


    class Meta:
        model = Mticket
        fields = ('ticket', 'partner','name','cni','observation' )
        widgets = {
            #'numero_colis': Textarea(attrs={'cols': 80, 'rows': 20, 'readonly': True}),
            #'dateheure': DateTimePickerInput(), # default date-format %m/%d/%Y will be used
        }

