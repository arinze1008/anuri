# encoding: utf-8
from __future__ import unicode_literals
from django.utils.translation import pgettext_lazy
from collections import defaultdict

from django import forms
from .models import SipExtension,AgentConf, HoaxSetting, HoaxDuration

CHOICES = (('Weakly', 'Weakly',), ('Monthly', 'Monthly',), ('Days', 'Days',))

class ExtensionForm(forms.ModelForm):
    class Meta:
        model = SipExtension
        widgets = {
            'secret': forms.PasswordInput(),
        }
        exclude = []

    def clean(self):
        clean_data = super(ExtensionForm, self).clean()
        return clean_data

class AgentsForm(forms.ModelForm):
    class Meta:
        model = AgentConf
        exclude = []

    def clean(self):
        clean_data = super(AgentsForm, self).clean()
        return clean_data

class ExtForm(forms.ModelForm):
    class Meta:
        model = SipExtension
        widgets = {
            'secret': forms.PasswordInput(),
        }
        exclude = []

    def __init__(self, *args, **kwargs):
        super(ExtForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            for field in self.fields.keys():
                self.fields[field].widget.attrs['readonly'] = True
    def clean(self):
        clean_data = super(ExtForm, self).clean()
        return clean_data

class AgentForm(forms.ModelForm):
    class Meta:
        model = AgentConf
        exclude = []

    def __init__(self, *args, **kwargs):
        super(AgentForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            for field in self.fields.keys():
                self.fields[field].widget.attrs['readonly'] = True

    def clean(self):
        clean_data = super(AgentForm, self).clean()
        return clean_data

# class AgentForm(forms.ModelForm):
#     name = forms.ModelChoiceField(queryset=Session.objects.all())
#     extension = forms.ModelChoiceField(queryset=Fees.objects.all())

class HoaxSettingForm(forms.ModelForm):
    review_period = forms.ModelChoiceField(queryset=HoaxDuration.objects.all())
    class Meta:
        model = HoaxSetting
        exclude = []

    def clean(self):
        clean_data = super(HoaxSettingForm, self).clean()
        return clean_data