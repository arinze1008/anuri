# encoding: utf-8
from __future__ import unicode_literals

from collections import defaultdict

from django import forms
from .models import Profile, Callgroup, Agency, Roles
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy
from phonenumber_field.formfields import PhoneNumberField
from extension.models import SipExtension
try:
    from Asterisk import Manager
except ImportError:
    Manager = None

class ProfileForm(forms.Form):

    username = forms.EmailField(label=pgettext_lazy('Form field', 'Username'),
                                max_length=75)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput,
                               label=pgettext_lazy('Form field', 'Password'))
    confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput,
                                       label=pgettext_lazy('Form field', 'Confirm Password'))
    first_name = forms.CharField(max_length=100,
                               label=pgettext_lazy('Form field', 'First Name'))
    last_name = forms.CharField(max_length=100,
                                label=pgettext_lazy('Form field', 'Last Name'))
    callgroup = forms.ModelChoiceField(queryset=Callgroup.objects.all(),
                                       label=pgettext_lazy('Form field', 'Group'))
    phone = PhoneNumberField(max_length=100,label = pgettext_lazy('Form field', 'Phone Number'), required=False)
    extension = forms.ModelChoiceField(queryset=SipExtension.objects.all(),
                                       label=pgettext_lazy('Form field', 'Extension'), required = False)
    agency = forms.ModelChoiceField(queryset=Agency.objects.all(),
                                       label=pgettext_lazy('Form field', 'Agency'), required=False)
    role = forms.ModelChoiceField(queryset=Roles.objects.all(),
                                       label=pgettext_lazy('Form field', 'Role'))


    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")

        return self.cleaned_data


class UserForm(forms.ModelForm):
    password = forms.CharField(max_length=100, widget=forms.PasswordInput,
                               label=pgettext_lazy('Form field', 'Password'), required=False)
    class Meta:
        model = Profile
        exclude = []
        widgets = {'user': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            for field in self.fields.keys():
                self.fields[field].widget.attrs['readonly'] = True
    def clean(self):
        clean_data = super(UserForm, self).clean()
        return clean_data

class UpdateForm(forms.ModelForm):
    password = forms.CharField(max_length=100, widget=forms.PasswordInput,
                               label=pgettext_lazy('Form field', 'Password'),required=False)
    extension = forms.ModelChoiceField(queryset=SipExtension.objects.all(), to_field_name="extension",
                                       label=pgettext_lazy('Form field', 'Extension'), required=True)
    class Meta:
        model = Profile
        exclude = []
        widgets = {'user': forms.HiddenInput()}

    def clean(self):
        clean_data = super(UpdateForm, self).clean()
        return clean_data

class UserExForm(forms.Form):
    name = forms.CharField(label=pgettext_lazy('Form field', 'Username'),
                                max_length=75, widget=forms.TextInput(attrs={'readonly': 'readonly'}), required=True)
    # extension = forms.CharField(label=pgettext_lazy('Form field', 'Extension'),
    #                             max_length=75, widget=forms.TextInput(attrs={'readonly': 'readonly'}), required=True)

    extension = forms.ModelChoiceField(queryset=SipExtension.objects.all(),to_field_name="extension",
                                       label=pgettext_lazy('Form field', 'Extension'), required=True)
    def clean(self):
        clean_data = super(UserExForm, self).clean()
        return clean_data