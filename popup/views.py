from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from .forms import AgentbreakForm,ComplaintForm,PhoneForm
from django.template.response import TemplateResponse
import json
from django.db.models import Sum, F, Count
from django.http import Http404, HttpResponse
from fm.views import AjaxCreateView, AjaxUpdateView, AjaxDeleteView
from .models import AgentBreak, State, Account, Complaint, Respondent,AgentDispatch,Community,AgentLiveCall
from report.models import AgentStatus,Queue
from rolepermissions.decorators import has_role_decorator
from django.shortcuts import get_object_or_404
from django_cron import CronJobBase, Schedule
from dal import autocomplete
from time import gmtime, strftime
from rolepermissions.decorators import has_permission_decorator
from extension.models import AgentConf
from report.models import Queue
import glob
import os
from datetime import timedelta
from datetime import datetime,date
from django.core import serializers
import time
from django.utils import timezone
try:
    from Asterisk import Manager
except ImportError:
    Manager = None
# Create your views here.

from .models import Notify, LoginLogout, Logout
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class NotifyList(APIView):

    def post(self, request, format=None):
        caller = request.data.get("caller")
        called = request.data.get("called")
        Notify.objects.create(caller=caller, called=called, state="")
        # show that the agent is online
        agent_ext_arr = called.split("/")
        print agent_ext_arr[1]
        agent_called = get_object_or_404(AgentConf, extension=agent_ext_arr[1])
        print agent_called
        AgentLiveCall.objects.filter(agent=agent_called).delete()
        AgentLiveCall.objects.create(name="ONLINE", agent=agent_called)
        return Response(status=status.HTTP_201_CREATED)

class LoginList(APIView):

    def post(self, request, format=None):
        agent = request.data.get("agent")
        agent_strip = agent.strip()
        agt_clean = agent_strip[1:-1]
        LoginLogout.objects.create(agent=agent)
        agent_called = get_object_or_404(AgentConf, extension=agt_clean)
        AgentLiveCall.objects.filter(agent=agent_called).delete()
        AgentLiveCall.objects.create(name="READY", agent=agent_called)
        return Response(status=status.HTTP_201_CREATED)

class LogoutList(APIView):

    def post(self, request, format=None):
        agent = request.data.get("agent")
        agent_strip = agent.strip()
        agt_clean = agent_strip[1:-1]
        Logout.objects.create(agent=agent)
        agent_called = get_object_or_404(AgentConf, extension=agt_clean)
        AgentLiveCall.objects.filter(agent=agent_called).delete()
        AgentLiveCall.objects.create(name="OFFLINE", agent=agent_called)
        manager = connect_to_asterisk()
        try:
            # Pause to prevent incoming call
            manager.QueuePause("tech_queue", agent_c, False)
        except Exception as e:
            print(e)
        finally:
            manager.close()
        return Response(status=status.HTTP_201_CREATED)


class EndcallList(APIView):
    def post(self, request, format=None):
        call_id = request.data.get("id")
        try:
        # Get the agent Id from the queue table
            print "collins"
            call_id = call_id.strip()
            call_id = call_id[1:-1]
            qu_obj = Queue.objects.filter(callid=call_id).last()
            Notify.objects.create(caller="", called="", state="")
            agent_c = qu_obj.agent
            agent_c_arr = agent_c.split("/")
            agent_end_call = AgentLiveCall.objects.filter(agent__extension=agent_c_arr[1]).last()
            agent_end_call.name = "WRAPUP"
            diff = datetime.now() - agent_end_call.time_out
            agent_end_call.spent = diff
            agent_end_call.status = "inactive"
            agent_end_call.save()
        except Exception as e:
            print (e)
        finally:
            pass

        manager = connect_to_asterisk()
        try:
            # Pause to prevent incoming call
            manager.QueuePause("tech_queue", agent_c, True)
        except Exception as e:
            print(e)
        finally:
            manager.close()

        return Response(status=status.HTTP_201_CREATED)

@login_required
# @has_permission_decorator('view_call_console')
def home(request, pk):
    return TemplateResponse(
        request, 'popup/console.html',
        {'my_agent': "Agent/{}".format(pk),"agent_pk":pk})


@login_required
# @has_permission_decorator('create_call_record')
def popup_create(request):
    user = request.user
    case = Account()
    try:
        user_agent = AgentConf.objects.get(agent=user.profile)
        my_agent = user_agent.extension
    except:
        my_agent = None
    chan = None
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
                            dispatch_case.dispatch_time = datetime.now()
                            dispatch_case.respondent = resp.agency.name
                            dispatch_case.save()

                agent_id = 'Agent/{}'.format(my_agent)
                # agent_wrap = AgentStatus.objects.get(agentid=agent_id,agentstatus="WRA")
                # agent_wrap.agentstatus = "READY"
                # agent_wrap.save()
                message = _('Your Case has been successfully dispatched.')
                messages.success(request, message)
                return HttpResponseRedirect(reverse('popup:popup_edit', kwargs={"pk": new_case.pk}))
            except Exception as e:
                print(e)
            finally:
                manager.close()
    else:
        try:
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
        except:
            pop_form = ComplaintForm()
            phone_form = PhoneForm()
        # try:
        #     case = Account.objects.get(phone=caller_num)
        # except Account.DoesNotExist:
        #     pass
            # case.state_auto = "Enugu"
    return render(
        request, 'popup/popup-create.html',
         {'pop_form': pop_form,'phone_form': phone_form,'channel': chan})

@login_required
# @has_permission_decorator('edit_call_record')
def popup_edit(request, pk):
    user = request.user
    user_agent = AgentConf.objects.get(agent=user.profile)
    my_agent = user_agent.extension
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
                    dispatch_case.dispatch_time = datetime.now()
                    dispatch_case.save()
        agent_id = 'Agent/{}'.format(my_agent)
        agent_end_call = AgentLiveCall.objects.filter(agent_id=agent_id).last()
        # agent_wrap = AgentStatus.objects.get(agentid=agent_id,agentstatus="PAUSE")
        agent_end_call.name = "READY"
        agent_end_call.save()
        manager = connect_to_asterisk()
        try:
            manager.QueuePause("tech_queue", agent_id, False)
        except Exception as e:
            print(e)
        finally:
            manager.close()
        # user = request.user
        # agent = user.profile
        # user_agent = AgentConf.objects.get(agent=agent)
        # manager = connect_to_asterisk()
        # try:
        #     manager.QueuePause("tech_queue", "Agent/{}".format(user_agent.extension), False)
        # except Exception as e:
        #     print(e)
        # finally:
        #     manager.close()
        message = _('Extension information successfully updated.')
        messages.success(request, message)
        return HttpResponseRedirect(reverse('popup:console',kwargs={'pk': int(my_agent)}))
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
    agent_rt = AgentStatus.objects.all()
    return agent_rt

def get_agent_status():
    agent_rt = AgentLiveCall.objects.all()
    return agent_rt


def get_agent(requests):
    user = requests.user
    agent_avail_dict = {}
    agent_row_list = []
    user_agent = AgentConf.objects.get(agent=user.profile)
    my_agent = user_agent.extension
    agent_id = 'Agent/{}'.format(my_agent)
    # agent_rt = AgentStatus.objects.exclude(agentid=agent_id)
    agent_rt = AgentStatus.objects.all()

    for row in agent_rt:
        agent_row = str(row.agentid).split('/')
        agenttconf = AgentConf.objects.get(extension=agent_row[1])
        agent_name = "{} {}".format(agenttconf.agent.first_name, agenttconf.agent.last_name)
        agent_avail_dict["name"] = agent_name
        agent_avail_dict["agent"] = 'Agent/{}'.format(agenttconf.extension)
        agent_row_list.append(agent_avail_dict)
        agent_avail_dict = {}
    # agent_rt = AgentStatus.objects.all().exclude(agentid=agent_id)

    return agent_row_list


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
    user = request.user
    exten = user.profile.extension
    agent_dict = {}
    agent_dict_all = {}
    agent_call_dict = {}
    break_dict ={}
    cases_dict = dict.fromkeys(["ticket_id", "caller_number","caller_name", "repondency_agency", "emergency", "location", "status","last_updated"],
                                  0)
    agent_on_dict = dict.fromkeys(["caller_number","agent_id","agent_name","status","duration","ConnectedLineNum"], 0)
    agent_avail_dict = dict.fromkeys(["agent_name", "agent_id", "status", "talk_time", "call_no"], 0)
    # file_path = os.path.join(settings.AUDIO_DIRS, 'test.txt')
    # print settings.AUDIO_DIRS[0];
    files = sorted(
        glob.iglob(settings.AUDIO_DIRS[0] + "/*.wav"), key=os.path.getctime, reverse=True)
    audios = [os.path.basename(x) for x in files]
    # agent_status = get_agents()
    agent_status = get_agent_status()
    agent_oncall = agent_on_call()

    for channel in agent_oncall:
        if channel.Application == "AppQueue" and channel.ChannelStateDesc == "Up" and len(channel.BridgedChannel) > 0:
            agent_on_dict["caller_number"] = channel.ConnectedLineNum
            agent_on_dict["status"] = "On Call"
            agent_on_dict["duration"] = channel.Duration
            agent_on_dict["ConnectedLineNum"] = ""
            queue_obj = Queue.objects.filter(callid=channel.BridgedUniqueID).last()
            agent_id = queue_obj.agent
            agent_id_arr = agent_id.split('/')
            agent_obj = AgentConf.objects.get(extension=agent_id_arr[1])
            agent_on_dict["agent_id"] = agent_id
            agent_on_dict["agent_name"] = "{} {}".format(agent_obj.agent.first_name,agent_obj.agent.last_name)
            agent_call_dict[agent_id] = agent_on_dict
            agent_on_dict = {}

    for row in agent_status:
        # agent_row = str(row.agentid).split('/')
        # agenttconf = AgentConf.objects.get(extension=agent_row[1])
        agent_name = "{} {}".format(row.agent.agent.first_name, row.agent.agent.last_name)
        agent_avail_dict["agent_name"] = agent_name
        agent_avail_dict["agent_id"] = "Agent/{}".format(row.agent.extension)
        agent_avail_dict["status"] = row.name

        my_date = strftime("%Y-%m-%d", gmtime())
        start_date = '{} 00:00:00'.format(my_date)
        end_date = '{} 23:59:00'.format(my_date)

        call_no = Queue.objects.filter(agent="Agent/{}".format(row.agent.extension),event="CONNECT", time__range=(start_date,end_date)).count()
        talk_times = Queue.objects.filter(agent="Agent/{}".format(row.agent.extension), event__in=['COMPLETECALLER', 'COMPLETEAGENT']
                                         , time__range=(start_date,end_date))
        tmp_talk_time = 0.0
        for rst in talk_times:
            tmp_talk_time += float(rst.data2)
        talk_time = time.strftime('%H:%M:%S', time.gmtime(tmp_talk_time))

        agent_avail_dict["talk_time"] = talk_time
        agent_avail_dict["call_no"] = call_no
        agent_dict["Agent/{}".format(row.agent.extension)] = agent_avail_dict
        agent_avail_dict = {}

    agency_incidence = AgentDispatch.objects.filter(dispatch_time__year=date.today().year,
                                                    dispatch_time__month=date.today().month,
                                                    dispatch_time__day=date.today().day).order_by(
        'dispatch_time').reverse()
    for agt_in in agency_incidence:
        cases_dict["ticket_id"]=agt_in.ticket_id
        try:
            compt = Complaint.objects.get(pk=agt_in.ticket_id)
            cases_dict["caller_number"] = compt.phone
            cases_dict["caller_name"] = compt.name
        except:
            cases_dict["caller_number"] = 0
            cases_dict["caller_name"] = "i"

        cases_dict["repondency_agency"] = agt_in.respondent
        cases_dict["emergency"] = agt_in.incidence
        cases_dict["location"] = agt_in.location
        cases_dict["status"] = agt_in.status
        cases_dict["last_updated"] = agt_in.dispatch_time
        agent_dict_all[agt_in.id]=cases_dict
        cases_dict = {}
    return render(
        request, 'popup/supervisor.html',
        {'audios': audios, 'agent_dict': agent_dict,"agent_dict_all":agent_dict_all,
         'agent_call_dict': agent_call_dict, 'break_dict': break_dict, "exten":exten,"agency_incidence":agency_incidence})

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
            AgentLiveCall.objects.filter(agent=user_agent).delete()
            AgentLiveCall.objects.create(name="BREAK", agent= user_agent)
        except Exception as e:
            print(e)
        finally:
            manager.close()

def transfer_agent(request):
    if request.is_ajax():
        available_agent = get_agent(request)
        if  available_agent:
            data = json.dumps(available_agent)
            # print data
            # data = serializers.serialize('json', available_agent)
            return HttpResponse(data, content_type='application/json')
        else:
            dict = {'name': "Nobody is Available"}
            data = json.dumps(dict)
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
    agent_break = AgentBreak.objects.filter(agent = user_agent).last()
    agent_live = AgentLiveCall.objects.filter(agent= user_agent).last()
    diff = datetime.now() - agent_break.time_out
    agent_break.spent = diff
    agent_break.status = "inactive"
    agent_break.save()
    agent_live.spent = diff
    agent_live.name = "READY"
    agent_live.status = "inactive"
    agent_live.save()
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

def transfer(request,channels):
    manager = connect_to_asterisk()
    try:
        info_array = channels.split('_')
        # if request.is_ajax():
        context = 'SIP/{}'.format(info_array[1])
        # priority = request.GET.get('priority')
        channel = info_array[2]
        totransfer = "Agent/{}".format(info_array[0])
        manager.Redirect(channel,context, totransfer)
        return HttpResponse(json.dumps({"HTTPRESPONSE": 1}), content_type="application/json")
        # else:
        #     raise Http404
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


