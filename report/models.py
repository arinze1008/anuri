from __future__ import unicode_literals

from django.db import models
from django.utils.translation import pgettext_lazy
from userprofile.models import Profile
# Create your models here.
class Cdr(models.Model):

    src = models.CharField(pgettext_lazy('User field', 'src'),
                           max_length=255, blank=True, null=True)
    dst = models.CharField(pgettext_lazy('User field', 'dst'),
                           max_length=255, blank=True, null=True)
    dcontext = models.CharField(pgettext_lazy('User field', 'dcontext'),
                                max_length=255, blank=True, null=True)
    clid = models.CharField(pgettext_lazy('User field', 'clid'),
                            max_length=255, blank=True, null=True)
    channel = models.CharField(pgettext_lazy('User field', 'channel'),
                               max_length=255, blank=True, null=True)
    dstchannel = models.CharField(pgettext_lazy('User field', 'dstchannel'),
                                  max_length=255, blank=True, null=True)
    lastapp = models.CharField(pgettext_lazy('User field', 'lastapp'),
                               max_length=255, blank=True, null=True)
    lastdata = models.CharField(pgettext_lazy('User field', 'lastdata'),
                                max_length=255, blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    billsec = models.IntegerField(blank=True, null=True)
    disposition = models.CharField(pgettext_lazy('User field', 'disposition'),
                                   max_length=255, blank=True, null=True)
    amaflags = models.IntegerField(blank=True, null=True)

    uniqueid = models.CharField(pgettext_lazy('User field', 'uniqueid'),
                                max_length=255, blank=True, null=True)
    calldate = models.DateTimeField(null=True, blank=True)


class Queue(models.Model):
    time = models.CharField(pgettext_lazy('Queue field', 'time'),
                           max_length=255, blank=True, null=True)
    callid = models.CharField(pgettext_lazy('Queue field', 'callid'),
                            max_length=255, blank=True, null=True)
    queuename = models.CharField(pgettext_lazy('Queue field', 'queuename'),
                            max_length=255, blank=True, null=True)
    agent = models.CharField(pgettext_lazy('Queue field', 'agent'),
                            max_length=255, blank=True, null=True)
    event = models.CharField(pgettext_lazy('Queue field', 'event'),
                            max_length=255, blank=True, null=True)
    data1 = models.CharField(pgettext_lazy('Queue field', 'data1'),
                            max_length=255, blank=True, null=True)
    data2 = models.CharField(pgettext_lazy('Queue field', 'data2'),
                            max_length=255, blank=True, null=True)
    data3 = models.CharField(pgettext_lazy('Queue field', 'data3'),
                            max_length=255, blank=True, null=True)
    data4 = models.CharField(pgettext_lazy('Queue field', 'data4'),
                            max_length=255, blank=True, null=True)
    data5 = models.CharField(pgettext_lazy('Queue field', 'data5'),
                            max_length=255, blank=True, null=True)

class AgentStatus(models.Model):
    agentid = models.CharField(pgettext_lazy('Agent field', 'agentid'),
                            max_length=255, blank=True, null=True)
    agentname = models.CharField(pgettext_lazy('Agent field', 'agentname'),
                            max_length=255, blank=True, null=True)
    agentstatus = models.CharField(pgettext_lazy('Agent field', 'agentstatus'),
                            max_length=255, blank=True, null=True)
    timestamp = models.CharField(pgettext_lazy('Agent field', 'timestamp'),
                            max_length=255, blank=True, null=True)
    callid = models.FloatField(pgettext_lazy('Agent field', 'callid'),
                            max_length=255, blank=True, null=True)
    queue = models.CharField(pgettext_lazy('Agent field', 'time'),
                            max_length=255, blank=True, null=True)

class BitAgentStatus(models.Model):
    agentid = models.CharField(pgettext_lazy('Agent field', 'agentid'),
                            max_length=255, blank=True, null=True)
    agentname = models.CharField(pgettext_lazy('Agent field', 'agentname'),
                            max_length=255, blank=True, null=True)
    agentstatus = models.CharField(pgettext_lazy('Agent field', 'agentstatus'),
                            max_length=255, blank=True, null=True)
    timestamp = models.CharField(pgettext_lazy('Agent field', 'timestamp'),
                            max_length=255, blank=True, null=True)
    callid = models.FloatField(pgettext_lazy('Agent field', 'callid'),
                            max_length=255, blank=True, null=True)
    queue = models.CharField(pgettext_lazy('Agent field', 'time'),
                            max_length=255, blank=True, null=True)

class CallStatus(models.Model):
    callid = models.CharField(pgettext_lazy('Call field', 'callis'),
                            max_length=255, blank=True, null=True)
    callerid = models.CharField(pgettext_lazy('Call field', 'callerid'),
                            max_length=255, blank=True, null=True)
    status = models.CharField(pgettext_lazy('Call field', 'status'),
                            max_length=255, blank=True, null=True)
    timestamp = models.CharField(pgettext_lazy('Call field', 'timestamp'),
                            max_length=255, blank=True, null=True)
    queue = models.FloatField(pgettext_lazy('Call field', 'queue'),
                            max_length=255, blank=True, null=True)
    position = models.CharField(pgettext_lazy('Call field', 'position'),
                            max_length=255, blank=True, null=True)
    originalposition = models.CharField(pgettext_lazy('Call field', 'originalposition'),
                             max_length=255, blank=True, null=True)
    holdtime = models.CharField(pgettext_lazy('Call field', 'holdtime'),
                             max_length=255, blank=True, null=True)
    keypressed = models.CharField(pgettext_lazy('Call field', 'keypressed'),
                             max_length=255, blank=True, null=True)
    callduration = models.CharField(pgettext_lazy('Call field', 'callduration'),
                             max_length=255, blank=True, null=True)

class Hours(models.Model):
    name = models.CharField(pgettext_lazy('Hour field', 'Hour'),
                             max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class Minutes(models.Model):
    name = models.CharField(pgettext_lazy('Hour field', 'Hour'),
                             max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class QueryTable(models.Model):
    year_from = models.CharField(max_length=255, blank=True, null=True)
    month_from = models.CharField(max_length=255, blank=True, null=True)
    day_from = models.CharField(max_length=255, blank=True, null=True)
    year_to = models.CharField(max_length=255, blank=True, null=True)
    month_to = models.CharField(max_length=255, blank=True, null=True)
    day_to = models.CharField(max_length=255, blank=True, null=True)
    hour_from = models.CharField(max_length=255, blank=True, null=True)
    minute_from = models.CharField(max_length=255, blank=True, null=True)
    hour_to = models.CharField(max_length=255, blank=True, null=True)
    minute_to = models.CharField(max_length=255, blank=True, null=True)
    agents = models.TextField( blank=True, null=True)
    ext = models.TextField(blank=True, null=True)
