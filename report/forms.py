# encoding: utf-8
from __future__ import unicode_literals
from django.utils.translation import pgettext_lazy
from collections import defaultdict
from extension.models import AgentConf
from .models import Hours, Minutes
from django import forms
from django.forms import SelectDateWidget
from bootstrap3_datetime.widgets import DateTimePicker
from easy_select2 import Select2Multiple

class SearchForm(forms.Form):
    year_from = forms.ModelChoiceField(queryset=Hours.objects.all())
    year_to = forms.ModelChoiceField(queryset=Hours.objects.all())
    month_from = forms.ModelChoiceField(queryset=Minutes.objects.all())
    month_to = forms.ModelChoiceField(queryset=Minutes.objects.all())
    day_from = forms.ModelChoiceField(queryset=Minutes.objects.all())
    day_to = forms.ModelChoiceField(queryset=Minutes.objects.all())
    hours_from = forms.ModelChoiceField(queryset=Hours.objects.all())
    hours_to = forms.ModelChoiceField(queryset=Hours.objects.all())
    minutes_from = forms.ModelChoiceField(queryset=Minutes.objects.all())
    minutes_to = forms.ModelChoiceField(queryset=Minutes.objects.all())

    def clean(self):
        clean_data = super(SearchForm, self).clean()
        return clean_data

class SetForm(forms.Form):
    date_from = forms.DateTimeField(
        required=True,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm"}))
    date_to = forms.DateTimeField(
        required=True,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm"}))

    agents = forms.ModelChoiceField(queryset=AgentConf.objects.all(),to_field_name='extension', required=False, widget=Select2Multiple(
    ))
    # def clean(self):
    #     clean_data = super(SetForm, self).clean()
    #     return clean_data

