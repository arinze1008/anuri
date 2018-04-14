from __future__ import unicode_literals
from django.utils.translation import pgettext_lazy
from django.db import models
from userprofile.models import Profile
from .config import (
    TYPE_CHOICES,
    CANREINVITE_CHOICES,
    QUALIFY_CHOICES,
    NAT_CHOICES,
    SRVLOOPUP_CHOICES,
)
# Create your models here.
class Device(models.Model):
   name = models.CharField(pgettext_lazy('User field', 'first name'),
                       max_length=256)

   def __str__(self):
        return self.name

class Sync(models.Model):
    ip = models.CharField(pgettext_lazy('Sync field','ip'),max_length=256)
    ext = models.CharField(pgettext_lazy('Sync field','ext'),max_length=256)

    def __str__(self):
        return self.ip

class SipExtension(models.Model):
    name = models.CharField(pgettext_lazy('Extension field', 'Display Name'), max_length=255)
    extension = models.CharField(pgettext_lazy('Extension field', 'User Extension'),unique=True,
                            max_length=255)
    type = models.CharField(pgettext_lazy('Extension field', 'type'), choices=TYPE_CHOICES, default='peer', max_length=255)
    secret = models.CharField(pgettext_lazy('Extension field', 'secret'), max_length=255)
    username = models.CharField(pgettext_lazy('Extension field', 'username'), max_length=255)
    host = models.CharField(pgettext_lazy('Extension field', 'host'),default='dynamic', max_length=255)
    fromuser = models.CharField(pgettext_lazy('Extension field', 'fromuser'), max_length=255, blank=True, null=True)
    fromdomain = models.CharField(pgettext_lazy('Extension field', 'fromdomain'), max_length=255, blank=True, null=True)
    canreinvite = models.CharField(pgettext_lazy('Extension field', 'canreinvite'),choices=CANREINVITE_CHOICES, default='no', max_length=255)
    insecure = models.CharField(pgettext_lazy('Extension field', 'insecure'), default='invite,port', max_length=255)
    qualify = models.CharField(pgettext_lazy('Extension field', 'qualify'), choices=QUALIFY_CHOICES, default='yes', max_length=255)
    nat = models.CharField(pgettext_lazy('Extension field', 'nat'),choices=NAT_CHOICES, default='yes', max_length=255)
    context = models.CharField(pgettext_lazy('Extension field', 'context'), default='from-internal', max_length=255)
    bindport = models.CharField(pgettext_lazy('Extension field', 'bindport'), default='5060', max_length=255)
    srvlookup = models.CharField(pgettext_lazy('Extension field', 'srvloopup'),choices=SRVLOOPUP_CHOICES, default='yes',max_length=255)
    disallow = models.CharField(pgettext_lazy('Extension field', 'disallow'), default='all', max_length=255)
    allow = models.CharField(pgettext_lazy('Extension field', 'allow'), default='ulaw,alaw,gsm', max_length=255)

    def __str__(self):
        return self.extension

class AgentConf(models.Model):
    extension = models.CharField(pgettext_lazy('Agent field', 'AgentID'),
                            max_length=255,default="101")
    extension_secret = models.CharField(pgettext_lazy('Agent field', 'Password'),
                            max_length=255)
    agent = models.ForeignKey(Profile)

    def __str__(self):
        return self.agent.first_name +" {}".format(self.agent.last_name)

class Hoax(models.Model):
    name = models.CharField(
        pgettext_lazy('Hoax field', 'Review Period Name'),
        max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class HoaxSetting(models.Model):
    hoax_type = models.ForeignKey(Hoax, related_name='hoax', blank=True, null=True)
    review_period = models.CharField(
        pgettext_lazy('Hoax field', 'Review Period'),
        max_length=255, blank=True, null=True)
    number_hoax = models.CharField(
        pgettext_lazy('Hoax field', 'Allowable Frequency'),
        max_length=255, blank=True, null=True)
    placed_hoax = models.CharField(
        pgettext_lazy('Hoax field', 'Period Placed as Hoax (days)'),
        max_length=255, blank=True, null=True)
    in_next_days = models.CharField(
        pgettext_lazy('Hoax field', 'Number of Days'),
        max_length=255, blank=True, null=True)


class HoaxDuration(models.Model):
    name = models.CharField(
        pgettext_lazy('Hoax field', 'Review Period Name'),
        max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

