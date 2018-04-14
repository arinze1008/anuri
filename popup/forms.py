# encoding: utf-8
from __future__ import unicode_literals
from django import forms
from django.forms import Textarea
from django.utils.translation import pgettext_lazy
from ckeditor.widgets import CKEditorWidget
from dal import autocomplete
try:
    from Asterisk import Manager
except ImportError:
    Manager = None
from .models import AgentBreak, Account,  State, Complaint
# from django_select2.forms import Select2Widget

CHOICES = (('Yes', 'Yes',), ('No', 'No',))
LOC_CHOICES = (('Yes', 'Yes',), ('No', 'No',))

# class AccountForm(forms.Form):
#     class Meta:
#         model = Account
#         exclude = []
#
#     def clean(self):
#         clean_data = super(AccountForm, self).clean()
#         return clean_data

class ComplaintForm(forms.ModelForm):
    # phone = forms.CharField(max_length=100,
    #                             label=pgettext_lazy('Form field', 'Phone Number'), required = True)
    injured_citizen = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES,
                                        label=pgettext_lazy('Form field', 'Injured Citizen'))

    class Meta:
        model = Complaint
        exclude = []
        widgets = {
            'state': autocomplete.ModelSelect2(
                'state-autocompletes'
            ),
            'community': autocomplete.ModelSelect2(
                'create-autocomplete'
            )
        }

class AgentbreakForm(forms.ModelForm):

    class Meta:
        model = AgentBreak
        exclude = ('agent','time_in','time_out', "time_spent")


class PhoneForm(forms.Form):
    phones = forms.CharField(label=pgettext_lazy('Form field', 'Number'),
                                max_length=75,required=False)

    def clean(self):
        clean_data = super(PhoneForm, self).clean()
        return clean_data

