from __future__ import unicode_literals
from django import forms
from django.forms import Textarea
from django.utils.translation import pgettext_lazy
from .models import Dispatch
from popup.models import LocationContact
from dal import autocomplete
try:
    from Asterisk import Manager
except ImportError:
    Manager = None

class DispatchForm(forms.ModelForm):

    class Meta:
        model = Dispatch
        exclude = []

class LocationContactForm(forms.ModelForm):

    class Meta:
        model = LocationContact
        exclude = ['contact']
        widgets = {

            'community': autocomplete.ModelSelect2(
                'create-autocomplete'
            )
        }
