from __future__ import unicode_literals

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db import models
from django.utils import timezone
from django.utils.translation import pgettext_lazy
from django_countries.fields import Country, CountryField

class Callgroup(models.Model):
    name = models.CharField (pgettext_lazy('User field', 'first name'),
        max_length = 256)
    def __str__(self):
        return self.name

class Extension(models.Model):
    name = models.CharField(pgettext_lazy('User field', 'first name'),
                            max_length=256)
    def __str__(self):
        return self.name

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


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=None)
    first_name = models.CharField(
        pgettext_lazy('User field', 'first name'),
        max_length=256)
    last_name = models.CharField(
        pgettext_lazy('User field', 'last name'),
        max_length=256)
    callgroup = models.ForeignKey(Callgroup, related_name='callgroup')
    extension = models.ForeignKey(Extension, related_name='extension')
    phone = models.CharField(
        pgettext_lazy('User field', 'phone number'),
        max_length=30, blank=True)

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name_plural = "Profile"
