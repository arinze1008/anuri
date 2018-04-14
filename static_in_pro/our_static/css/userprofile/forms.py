# encoding: utf-8
from __future__ import unicode_literals

from collections import defaultdict

from django import forms
from .models import Profile
from django.utils.translation import ugettext_lazy as _
from datetimewidget.widgets import DateWidget
class ProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(label=_("Date of Birth"), required=False,
                                      widget=DateWidget(usel10n=True, bootstrap_version=3, )
                                      )
    AUTOCOMPLETE_MAPPING = (
        ('first_name', 'first_name'),
        ('last_name', 'last_name'),
        ('middle_name', 'middle_name'),
        ('street_address', 'street_address'),
        ('registration_number', 'registration_number'),
        ('department', 'department'),
        ('city', 'city'),
        ('postal_code', 'postal-code'),
        ('country', 'country'),
        ('phone', 'tel'),
    )

    class Meta:
        model = Profile
        exclude = []
        widgets = {'user': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        autocomplete_type = kwargs.pop('autocomplete_type', None)
        super(ProfileForm, self).__init__(*args, **kwargs)
        autocomplete_dict = defaultdict(
            lambda: 'off', self.AUTOCOMPLETE_MAPPING)
        for field_name, field in self.fields.items():
            if autocomplete_type:
                autocomplete = '%s %s' % (
                    autocomplete_type, autocomplete_dict[field_name])
            else:
                autocomplete = autocomplete_dict[field_name]
            field.widget.attrs['autocomplete'] = autocomplete

    def clean(self):
        clean_data = super(ProfileForm, self).clean()
        return clean_data

