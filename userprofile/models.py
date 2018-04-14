from __future__ import unicode_literals

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db import models
from django.utils import timezone
from django.utils.translation import pgettext_lazy
from phonenumber_field.modelfields import PhoneNumberField

from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Roles(models.Model):
    name = models.CharField (pgettext_lazy('Role field', 'first name'),
        max_length =255)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Roles"


class Agency(models.Model):
    name = models.CharField (pgettext_lazy('Agency field', 'first name'),
        max_length =255)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Agencies"

@python_2_unicode_compatible
class Emergency(models.Model):
    name = models.CharField(pgettext_lazy('Emergency field', 'Emergency name'),
                            max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Emergencies"

class Respondent(models.Model):
    agency = models.ForeignKey(Agency, related_name="reagency")
    emergency = models.ForeignKey(Emergency, related_name="respondent")

    def __str__(self):
        return self.agency.name

    class Meta:
        verbose_name_plural = "Respondents"
@python_2_unicode_compatible
class Callgroup(models.Model):
    name = models.CharField (pgettext_lazy('User field', 'first name'),
        max_length =255)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Call Groups"


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, is_staff=False,
                    is_active=True, **extra_fields):
        'Creates a User with the given username, email and password'
        email = UserManager.normalize_email(email)
        user = self.model(email=email, is_active=is_active,
                          is_staff=is_staff, **extra_fields)
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        return self.create_user(email, password, is_staff=True,
                                is_superuser=True, **extra_fields)

class User(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(
        pgettext_lazy('User field', 'staff status'),
        default=False)
    is_active = models.BooleanField(
        pgettext_lazy('User field', 'active'),
        default=False)
    date_joined = models.DateTimeField(
        pgettext_lazy('User field', 'date joined'),
        default=timezone.now, editable=False)


    USERNAME_FIELD = 'email'

    objects = UserManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

@python_2_unicode_compatible
class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=None)
    first_name = models.CharField(
        pgettext_lazy('User field', 'first name'),
        max_length=255)
    last_name = models.CharField(
        pgettext_lazy('User field', 'Last name'),
        max_length=255)
    callgroup = models.ForeignKey(Callgroup, related_name='callgroup', null=True, blank=True)
    phone = PhoneNumberField(blank=True)
    extension = models.CharField(
        pgettext_lazy('User field', 'Extension'),
        max_length=255, null=True, blank=True)
    role = models.ForeignKey(Roles, related_name='roles',default=1)
    agency = models.ForeignKey(Agency, related_name='agency', null=True, blank=True)
    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name_plural = "Profiles"

@python_2_unicode_compatible
class Agents(models.Model):
    name = models.CharField(pgettext_lazy('Agents field', 'Name'), max_length=255)
    extension = models.CharField(pgettext_lazy('Agents field', 'extension'), max_length=255)

    def __str__(self):
        return self.name

class AgentSession(models.Model):
    agent = models.ForeignKey(Profile, related_name='agentss')
    session_time = models.DurationField(blank=True, null=True)

    def __str__(self):
        return 'Agents'