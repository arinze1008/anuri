from __future__ import unicode_literals

from django.db import models
from django.utils.translation import pgettext_lazy
from django.utils.encoding import python_2_unicode_compatible
from userprofile.models import Profile, Agency
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
@python_2_unicode_compatible
class Status(models.Model):
    name = models.CharField(pgettext_lazy('Status field', 'Name'),
                            max_length=255)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Status"
@python_2_unicode_compatible
class Reason(models.Model):
    name = models.CharField(pgettext_lazy('Reason field', 'Name'),
                            max_length=255)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Reason"


@python_2_unicode_compatible
class Resolved(models.Model):
    name = models.CharField(pgettext_lazy('Resolved field', 'Name'),
                            max_length=255)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Resolution"


class Dispatch(models.Model):
    status = models.ForeignKey(Status, related_name="status")
    resolution = models.ForeignKey(Resolved, related_name="resolves", blank=True, null=True)
    respondent_name = models.CharField(
        pgettext_lazy('Dispatch field', 'respondent name'),
        max_length=255, blank=True, null=True)
    respondent_phone = models.CharField(
        pgettext_lazy('Dispatch field', 'respondent phone'),
        max_length=255, blank=True, null=True)
    respondent_location = models.CharField(
        pgettext_lazy('Dispatch field', 'respondent location'),
        max_length=255, blank=True, null=True)
    ticket_id = models.CharField(
        pgettext_lazy('Dispatch field', 'Ticket Id'),
        max_length=255, blank=True, null=True)
    officer_reachout_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    entered_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='dispatchuser', null=True, blank=True)
    agency = models.ForeignKey(Agency, related_name='dispatch_agency', null=True, blank=True)
    note = models.TextField()
    last_note = models.TextField(blank=True, null=True)
    reason = models.ForeignKey(Reason, related_name="reason", blank=True, null=True)


