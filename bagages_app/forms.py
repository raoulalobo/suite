#https://docs.djangoproject.com/fr/2.2/topics/forms/modelforms/

from django import forms
from .models import Voyage , Bagage
from django.forms import ClearableFileInput , Textarea
#from bootstrap_datepicker_plus import DateTimePickerInput
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
from django.utils.translation import gettext_lazy as _ # A quoi ca sert ?


class VoyageForm(forms.ModelForm):


    class Meta:

        model = Voyage
        fields = ('chauffeur','bagagiste','destination','immatriculation','observation' )


class BagageForm(forms.ModelForm):

    class Meta:

        model = Bagage
        fields = ('owner_name', 'owner_address','seat','quantity','image', 'observation')
