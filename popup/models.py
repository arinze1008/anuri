from __future__ import unicode_literals
from django.utils.translation import pgettext_lazy
from django.db import models
from userprofile.models import Profile, Respondent, Emergency
from django.utils.encoding import python_2_unicode_compatible
from smart_selects.db_fields import ChainedForeignKey, ChainedManyToManyField
from channels.binding.websockets import WebsocketBinding
from extension.models import AgentConf
# Create your models here.
@python_2_unicode_compatible
class INumber(models.Model):
    name = models.CharField(pgettext_lazy('priority field', 'Name'),
                            max_length=255)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Number of Incidence"


# for websocket
class Notify(models.Model):
    caller =  models.CharField(max_length=100, blank=True, default='')
    called = models.CharField(max_length=100, blank=True, default='')
    state = models.CharField(max_length=100, blank=True, default='')


# for websocket
class LoginLogout(models.Model):
    agent =  models.CharField(max_length=100, blank=True, default='')


# for websocket
class Logout(models.Model):
    agent =  models.CharField(max_length=100, blank=True, default='')


@python_2_unicode_compatible
class Grade(models.Model):
    phone = models.CharField(pgettext_lazy('hoax field', 'Phone'),
                            max_length=255)
    priority = models.CharField(pgettext_lazy('priority field', 'Priority'),
                            max_length=255)
    created_at = models.DateTimeField(("Created at"), auto_now_add=True)


    def __str__(self):
        return self.phone


@python_2_unicode_compatible
class Breaks(models.Model):
    name = models.CharField(pgettext_lazy('break field', 'Name'),
                             max_length=255)
    description = models.CharField(pgettext_lazy('break field', 'Description'),
                            max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Breaks"


class AgentBreak(models.Model):
    breaks = models.ForeignKey(Breaks,related_name='breaks')
    agent = models.ForeignKey(AgentConf)
    time_out = models.DateTimeField(auto_now_add=True)
    time_in = models.DateTimeField(auto_now=True)
    spent = models.CharField(max_length=100,blank=True, null=True)
    status = models.CharField(max_length=10, default="active",blank=True, null=True)

    def __str__(self):
        return  self.breaks.name


class AgentLiveCall(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    agent = models.ForeignKey(AgentConf)
    time_out = models.DateTimeField(auto_now_add=True)
    time_in = models.DateTimeField(auto_now=True)
    spent = models.CharField(max_length=100,blank=True, null=True)
    status = models.CharField(max_length=10, default="active",blank=True, null=True)

    def __str__(self):
        return  self.name


@python_2_unicode_compatible
class Geopolitical(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Geopolitical Zones"


@python_2_unicode_compatible
class State(models.Model):
    geopolitical = models.ForeignKey(Geopolitical)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "State"

@python_2_unicode_compatible
class Lga(models.Model):
    state = models.ForeignKey(State)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "LGA"

@python_2_unicode_compatible
class Community(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Communities"


class Account(models.Model):
    state_auto = models.CharField(
        pgettext_lazy('Account field', 'State'),
        max_length=255, blank=True, null=True)
    lga_auto = models.CharField(
        pgettext_lazy('Account field', 'LGA'),
        max_length=255, blank=True, null=True)
    community = models.CharField(
        pgettext_lazy('Account field', 'community'),
        max_length=255, blank=True, null=True)

    location_auto = models.CharField(
        pgettext_lazy('Account field', 'location'),
        max_length=255, blank=True, null=True)

    latitude = models.CharField(
        pgettext_lazy('Account field', 'Latitude'),
        max_length=255, blank=True, null=True)
    longitude = models.CharField(
        pgettext_lazy('Account field', 'Longitude'),
        max_length=255, blank=True, null=True)
    phone = models.CharField(
        pgettext_lazy('Account field', 'phone'),
        max_length=255, blank=True, null=True)
    first_name = models.CharField(
        pgettext_lazy('Account field', 'first name'),
        max_length=255, blank=True, null=True)
    last_name = models.CharField(
        pgettext_lazy('Account field', 'last name'),
        max_length=255, blank=True, null=True)


class Complaint(models.Model):
    state = models.ForeignKey(State, related_name="state", blank=True, null=True)
    name = models.CharField(
        pgettext_lazy('Complaint field', 'Name'),
        max_length=255, blank=True, null=True)
    phone = models.CharField(
        pgettext_lazy('Complaint field', 'phone'),
        max_length=255, blank=True, null=True)
    community = models.ForeignKey(
        Community, null=True, blank=True, related_name='community1'
    )
    location = models.CharField(
        pgettext_lazy('Complaint field', 'location'),
        max_length=255, blank=True, null=True)
    injured_citizen = models.CharField(
        pgettext_lazy('Complaint field', 'injured citizen'),
        max_length=255, blank=True, null=True)
    inc_number = models.ForeignKey(INumber, related_name="casuality_number", blank=True, null=True)

    channel = models.CharField(
        pgettext_lazy('Complaint field', 'channel'),
        max_length=255, blank=True, null=True)
    context = models.CharField(
        pgettext_lazy('Complaint field', 'context'),
        max_length=255, blank=True, null=True)
    emergencies = models.ManyToManyField(Emergency)
    respondent = ChainedManyToManyField(
        Respondent,
        chained_field="emergencies",
        chained_model_field="emergency",
        blank = False,
    )
    dispatch_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    entered_out = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    note = models.TextField(blank = True, null = True)
    agent = models.CharField(
        pgettext_lazy('Complaint field', 'agent'),
        max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class AgentDispatch(models.Model):
    ticket_id = models.CharField(
        pgettext_lazy('AgentDispatch field', 'Name'),
        max_length=255, blank=True, null=True)
    complaint = models.ForeignKey(Complaint,related_name ='complaint', blank=True, null=True)
    incidence= models.CharField(
        pgettext_lazy('AgentDispatch field', 'incidence'),
        max_length=255, blank=True, null=True)
    respondent = models.CharField(
        pgettext_lazy('AgentDispatch field', 'respondent'),
        max_length=255, blank=True, null=True)
    location = models.CharField(
        pgettext_lazy('AgentDispatch field', 'location'),
        max_length=255, blank=True, null=True)
    community = models.ForeignKey(
        Community, null=True, blank=True,related_name='community2'
    )
    #status of the case
    status = models.CharField(
        pgettext_lazy('AgentDispatch field', 'status'),
        max_length=255, blank=True, null=True)
    dispatch_time = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    entered_out = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    condition = models.CharField(
        pgettext_lazy('AgentDispatch field', 'Name'),
        max_length=255, blank=True, null=True)
    state = models.CharField(
        pgettext_lazy('AgentDispatch field', 'Name'),
        max_length=255, blank=True, null=True)
    sent_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    dispatch_duration = models.CharField(
        pgettext_lazy('AgentDispatch field', 'duration'),
        max_length=255, blank=True, null=True)

@python_2_unicode_compatible
class Contact(models.Model):
    name = models.CharField(pgettext_lazy('Status field', 'Name'),
                            max_length=255)
    phone = models.CharField(pgettext_lazy('Status field', 'Phone Number'),
                            max_length=255)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Contact"

class LocationContact(models.Model):
    community = models.ForeignKey(Community,related_name='com', blank=True, null=True)
    contact = models.ForeignKey(Contact,related_name='contact', blank=True, null=True)


class AgentDispatchBinding(WebsocketBinding):

    model = AgentDispatch
    stream = "incinfo"
    fields = ["ticket_id", "incidence","status"]

    @classmethod
    def group_names(cls, *args, **kwargs):
        return ["binding.values"]

    def has_permission(self, user, action, pk):
        return True

class NotifyBinding(WebsocketBinding):

    model = Notify
    stream = "supinfo"
    fields = ["caller", "called", "state"]

    @classmethod
    def group_names(cls, *args, **kwargs):
        return ["bind.values"]

    def has_permission(self, user, action, pk):
        return True

class PopBinding(WebsocketBinding):

    model = Notify
    stream = "popinfo"
    fields = ["caller", "called", "state"]

    @classmethod
    def group_names(cls, *args, **kwargs):
        return ["pop.values"]

    def has_permission(self, user, action, pk):
        return True

class LoginBinding(WebsocketBinding):

    model = LoginLogout
    stream = "logininfo"
    fields = ["agent"]

    @classmethod
    def group_names(cls, *args, **kwargs):
        return ["login.values"]

    def has_permission(self, user, action, pk):
        return True

class LogoutBinding(WebsocketBinding):

    model = Logout
    stream = "logoutinfo"
    fields = ["agent"]

    @classmethod
    def group_names(cls, *args, **kwargs):
        return ["logout.values"]

    def has_permission(self, user, action, pk):
        return True

class HoaxTracer(models.Model):
    number = models.CharField(
        pgettext_lazy('HoaxTracer field', 'number'),
        max_length=255, blank=True, null=True)
    set_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)

