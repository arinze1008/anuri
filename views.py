from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from .forms import CaseForm,AgentbreakForm,ComplaintForm,PhoneForm
from django.template.response import TemplateResponse
import json
from django.http import Http404, HttpResponse
from fm.views import AjaxCreateView, AjaxUpdateView, AjaxDeleteView
from .models import AgentBreak, Case, State, Account, Complaint, Respondent,AgentDispatch,Community
from report.models import AgentStatus
from rolepermissions.decorators import has_role_decorator
from django.shortcuts import get_object_or_404
from django_cron import CronJobBase, Schedule
from dal import autocomplete
from rolepermissions.decorators import has_permission_decorator
from extension.models import AgentConf
import glob
import os
from datetime import timedelta
from datetime import datetime,date

from django.utils import timezone
try:
    from Asterisk import Manager
except ImportError:
    Manager = None
# Create your views here.

from .models import Notify
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class NotifyList(APIView):

    def post(self, request, format=None):
        caller = request.data.get("caller")
        called = request.data.get("called")
        print (caller)
        Notify.objects.create(caller=caller, called=called, state="")
        return Response(status=status.HTTP_201_CREATED)

@login_required
# @has_permission_decorator('view_call_console')
def home(request):
    return TemplateResponse(
        request, 'popup/console.html',
        {'products': None})


@login_required
# @has_permission_decorator('create_call_record')
def popup_create(request):
    user = request.user
    case = Account()

    if request.method == 'GET':
        exten = request.GET.get('q')
    else:
        exten = None
    manager = connect_to_asterisk()
    phone_form = PhoneForm(request.GET or None)
    respondent_list = []
    if request.POST:
        pop_form = ComplaintForm(
            request.POST or None)
        if pop_form.is_valid():
            print (pop_form.cleaned_data['phone'])
            try:
                new_case = pop_form.save()
                emergencies = pop_form.cleaned_data['emergencies']
                respondents = pop_form.cleaned_data['respondent']
                for respondent in respondents:
                    respondent_list.append(respondent)
                for emergency in emergencies:

                    resps = Respondent.objects.filter(emergency=emergency)
                    for resp in resps:
                        if resp in respondent_list:
                            dispatch_case = AgentDispatch()
                            dispatch_case.ticket_id = new_case.pk
                            dispatch_case.community = new_case.community
                            dispatch_case.location = new_case.location
                            if new_case.state is None:
                                dispatch_case.state = None
                            else:
                                dispatch_case.state = new_case.state.name
                            dispatch_case.note = new_case.note
                            dispatch_case.status = "New"
                            dispatch_case.incidence = emergency
                            dispatch_case.respondent = resp.agency.name
                            dispatch_case.save()


                message = _('Your Case has been successfully dispatched.')
                messages.success(request, message)
                return HttpResponseRedirect(reverse('popup:popup_edit', kwargs={"pk": new_case.pk}))
            except Exception as e:
                print(e)
            finally:
                manager.close()
    else:
        channels = manager.CoreShowChannels()
        # Get the ringing extension
        caller_num = None
        caller_name = None
        chan = None
        context = None

        for channel in channels:
            if channel.CallerIDnum == exten:
                caller_name = channel.ConnectedLineName
                caller_num = channel.CallerIDnum
                chan = channel.Channel
                context = channel.Context
        data = {'phone': caller_num, 'name': caller_name,  'context': context,
                 'channel': chan,'agent': user.profile.last_name}

        pop_form = ComplaintForm(initial=data)
        phone_form = PhoneForm(initial={'phone': caller_num})
        # try:
        #     case = Account.objects.get(phone=caller_num)
        # except Account.DoesNotExist:
        #     pass
            # case.state_auto = "Enugu"
    return render(
        request, 'popup/popup-create.html',
         {'pop_form': pop_form,'phone_form': phone_form})

@login_required
# @has_permission_decorator('edit_call_record')
def popup_edit(request, pk):
    case = get_object_or_404(Complaint, pk=pk)
    respondent_list = []
    pop_form = ComplaintForm(request.POST or None, instance=case)
    phone_form = PhoneForm(request.GET or None)
    if pop_form.is_valid():
        inc_pop = pop_form.save(commit=False)
        inc_pop.status = 'Updated'
        inc_pop.save()
        emergencies = pop_form.cleaned_data['emergencies']
        respondents = pop_form.cleaned_data['respondent']
        for respondent in respondents:
            respondent_list.append(respondent)
        for emergency in emergencies:

            resps = Respondent.objects.filter(emergency=emergency)
            for resp in resps:
                if resp in respondent_list:
                    dispatch_case = AgentDispatch()
                    dispatch_case.ticket_id = inc_pop.pk
                    dispatch_case.community = inc_pop.community
                    dispatch_case.location = inc_pop.location
                    if inc_pop.state is None:
                        dispatch_case.state = None
                    else:
                        dispatch_case.state = inc_pop.state.name
                    dispatch_case.note = inc_pop.note
                    dispatch_case.status = "Updated"
                    dispatch_case.incidence = emergency
                    dispatch_case.respondent = resp.agency.name
                    dispatch_case.save()

        message = _('Extension information successfully updated.')
        messages.success(request, message)
        return HttpResponseRedirect(reverse('popup:console'))
    return render(
        request, 'popup/popup-edit.html',
        {'pop_form': pop_form, 'case': case,'phone_form': phone_form})


def connect_to_asterisk():
    ast_manager = None;
    try:
        ast_manager = Manager.Manager(address=('localhost',5038), username='smartcall',secret= 'welcome')

    except Exception as e:
        print("Issues with connecting to asterisk server, {}".format(e))

    return ast_manager

@login_required
def available_agent(request):
    if request.is_ajax():
        todo_items = ['Collins', 'Arinze', ]
        data = json.dumps(todo_items)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404

@login_required
def live_call(request):
    user = request.user
    exten = user.profile.extension
    # user_agent = AgentConf.objects.get(agent=user.profile)
    manager = connect_to_asterisk()
    try:
        channels = manager.CoreShowChannels()
    except Exception as e:
        print(e)
    finally:
        manager.close()
    return render(
        request, 'popup/calling.html',
        {'channels': channels, 'exten':exten})



def get_agents():
    agent_rt = AgentStatus.objects.filter(agentstatus='READY')
    return agent_rt



@login_required
def queue_call(request):
    manager = connect_to_asterisk()
    try:
        status = manager.QueueStatus()
        call_queue = status['tech_queue']['entries']
    except Exception as e:
        print(e)
    finally:
        manager.close()
    return render(
        request, 'popup/queued.html',
        {'tech_queue': call_queue})

@login_required
def calling_call(request):
    return render(
        request, 'popup/calling.html',
        {'pop_form': "ok"})

@login_required
def packed_call(request):
    manager = connect_to_asterisk()
    try:
        parked_calls = manager.ParkedCalls()

    except Exception as e:
        print(e)
    finally:
        manager.close()
    return render(
        request, 'popup/parked.html',
        {'parked_calls': parked_calls})

@login_required
def supervisor(request):
    from django.conf import settings
    agent_dict = {}
    break_dict = {}
    agent_break_dict = dict.fromkeys(["agent_name","agent_id"], 0)
    agent_avail_dict = dict.fromkeys(["agent_name","agent_id"], 0)
    files = sorted(
        glob.iglob(settings.AUDIO_DIRS[0] + "/*.wav"), key=os.path.getctime, reverse=True)
    audios = [os.path.basename(x) for x in files]
    available_agent = get_agents()
    agent_oncall = agent_on_call()
    agent_onbreak = agent_on_break()
    for row in agent_onbreak:
        agent_row = str(row.agentid).split('/')
        agenttconf = AgentConf.objects.get(extension=agent_row[1])
        agent_name = "{} {}".format(agenttconf.agent.first_name, agenttconf.agent.last_name)
        agent_break_dict["agent_name"] = agent_name
        agent_break_dict["agent_id"] = row.agentid
        break_dict[row.agentid] = agent_break_dict
        agent_break_dict = {}
    for row in available_agent:
        agent_row = str(row.agentid).split('/')
        agenttconf = AgentConf.objects.get(extension=agent_row[1])
        agent_name = "{} {}".format(agenttconf.agent.first_name, agenttconf.agent.last_name)
        agent_avail_dict["agent_name"] = agent_name
        agent_avail_dict["agent_id"] = row.agentid
        agent_dict[row.agentid] = agent_avail_dict
        agent_avail_dict = {}

    agency_incidence = AgentDispatch.objects.filter(dispatch_time__year=date.today().year,
                                                    dispatch_time__month=date.today().month,
                                                    dispatch_time__day=date.today().day).order_by(
        'dispatch_time').reverse()
    for agent in agency_incidence:
        print agent.location

    return render(
        request, 'popup/supervisor.html',
        {'audios': audios, 'agent_dict': agent_dict,
         'agent_oncall': agent_oncall, 'break_dict': break_dict})

def agent_on_call():
    manager = connect_to_asterisk()
    try:
        channels = manager.CoreShowChannels()
        return channels
    except Exception as e:
        print(e)
    finally:
        manager.close()


def agent_on_break():
    agent_rt = AgentStatus.objects.filter(agentstatus='PAUSE')
    return agent_rt


class AgentbreakCreateView(AjaxCreateView):
    form_class = AgentbreakForm

    def pre_save(self):
        user = self.request.user
        user_agent = AgentConf.objects.get(agent=user.profile)
        manager = connect_to_asterisk()
        try:
            manager.QueuePause("tech_queue", "Agent/{}".format(user_agent.extension),True)
            self.object.agent = user.profile
        except Exception as e:
            print(e)
        finally:
            manager.close()

def transfer_agent(request):
    if request.is_ajax():
        manager = connect_to_asterisk()
        # channels = manager.CoreShowChannels()
        # print(channels)
        agent = get_agents()
        data = json.dumps(agent)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404

def end_break(request):
    user = request.user
    agent = user.profile
    user_agent = AgentConf.objects.get(agent=agent)
    manager = connect_to_asterisk()
    try:
        manager.QueuePause("tech_queue", "Agent/{}".format(user_agent.extension), False)
    except Exception as e:
        print(e)
    finally:
        manager.close()
    agent_break = AgentBreak.objects.filter(agent_id=agent).last()
    diff = datetime.now() - agent_break.time_out
    agent_break.time_spent = diff
    agent_break.save()
    return render(
        request, 'popup/console.html')


def spy(from_exten, where_listen,  option=None):
    manager = connect_to_asterisk()
    options = ',q'
    if option:
        options = options + option
    try:
        # create a originate call for Spy a exten
        monitor =  manager.Originate('Local/'+ from_exten+'@monitoring',
                                         application='ChanSpy',
                                         data='Agent/'+ where_listen + options,
                                         async='yes')

    except Exception as e:
        print(e)
    finally:
        manager.close()


def call_spy(channel, to_exten,  with_whisper=False):
    try:
        return spy(channel, to_exten, with_whisper)
    except Exception as e:
        print(e)
        return {}


def whisper(request):
    if request.is_ajax():
        channel = request.GET.get('fromexten')
        to_exten = request.GET.get('toexten')
        call_spy(channel, to_exten, 'w')
        json_data = json.dumps({"HTTPRESPONSE": 1})
        # json data is just a JSON string now.
        return HttpResponse(json_data, content_type="application/json")
    else:
        raise Http404


def myspy(request):
    if request.is_ajax():
        channel = request.GET.get('fromexten')
        to_exten = request.GET.get('toexten')
        # caller = request.GET.get('caller')
        call_spy(channel, to_exten)
        return HttpResponse(json.dumps({"HTTPRESPONSE": 1}), content_type="application/json")
    else:
        raise Http404
def barge(request):
    if request.is_ajax():
        channel = request.GET.get('fromexten')
        to_exten = request.GET.get('toexten')
        call_spy(channel, to_exten, 'B')

        return HttpResponse(json.dumps({"HTTPRESPONSE": 1}), content_type="application/json")
    else:
        raise Http404

def hangup(request):
    manager = connect_to_asterisk()
    try:
        if request.is_ajax():
            channel = request.GET.get('chan')
            manager.Hangup(channel)
            return HttpResponse(json.dumps({"HTTPRESPONSE": 1}), content_type="application/json")
        else:
            raise Http404
    except Exception as e:
        print(e)
    finally:
        manager.close()

def transfer(request):
    manager = connect_to_asterisk()
    try:
        if request.is_ajax():
            context = request.GET.get('context')
            priority = request.GET.get('priority')
            channel = request.GET.get('channel')
            totransfer = request.GET.get('totransfer')
            manager.Redirect(channel,context, totransfer, priority)
            return HttpResponse(json.dumps({"HTTPRESPONSE": 1}), content_type="application/json")
        else:
            raise Http404
    except Exception as e:
        print(e)
    finally:
        manager.close()

def call_recording(request):
    for file in os.listdir("/mydir"):
        if file.endswith(".txt"):
            print(file)

def breaks(request):
    return render(
        request, 'popup/console_break.html')


class StateAutocompletes(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return State.objects.none()

        qs = State.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs

class CreateAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Community.objects.none()

        qs = Community.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs


