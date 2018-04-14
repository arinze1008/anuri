import os, errno
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ExtensionForm, ExtForm, AgentsForm,AgentForm,HoaxSettingForm
from django.template.response import TemplateResponse
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .tables import ExtTable, AgentTable, HoaxSettingTable
from .models import SipExtension, AgentConf, HoaxSetting
from rolepermissions.decorators import has_role_decorator
try:
    from Asterisk import Manager
except ImportError:
    Manager = None
# Create your views here.

@login_required
@has_role_decorator('admin')
def ext_detail(request, pk):
    ext = get_object_or_404(SipExtension, pk=pk)
    ext_form = ExtForm(request.POST or None, instance=ext)

    return render(
        request, 'extension/ext-detail.html',
        {'ext_form': ext_form, 'ext': ext})

def connect_to_asterisk():
    try:
        ast_manager = Manager.Manager(address=('localhost',5038), username='smartcall',secret= 'welcome')

    except Exception as e:
        print("Issues with connecting to asterisk server, {}".format(e))

    return ast_manager

@login_required
@has_role_decorator('admin')
def ext_create(request):
    ext_form = ExtensionForm(
        request.POST or None)
    if ext_form.is_valid():
        ext = ext_form.save()
        create_sip();
        manager = connect_to_asterisk()
        try:
            channels = manager.Command("sip reload")
        except Exception as e:
            print(e)
        finally:
            manager.close()
        message = _('Your extension has been successfully created.')
        messages.success(request, message)
        return HttpResponseRedirect(reverse('ext:ext-manage'))
    return TemplateResponse(
        request, 'extension/ext-create.html',
        {'ext_form': ext_form})



@login_required
@has_role_decorator('admin')
def ext_edit(request, pk):
    sipext = get_object_or_404(SipExtension, pk=pk)
    ext_form = ExtensionForm(request.POST or None, instance=sipext)
    if ext_form.is_valid():
        ext_form.save()
        create_sip();
        message = _('Extension information successfully updated.')
        messages.success(request, message)
        return HttpResponseRedirect(reverse('ext:ext-manage'))
    return render(
        request, 'extension/ext-edit.html',
        {'ext_form': ext_form,'sipext': sipext})

@login_required
@has_role_decorator('admin')
def agent_edit(request, pk):
    sipext = get_object_or_404(AgentConf, pk=pk)
    agent_form = AgentsForm(request.POST or None, instance=sipext)
    if agent_form.is_valid():
        agent_form.save()
        create_agent();
        message = _('Agent information successfully updated.')
        messages.success(request, message)
        return HttpResponseRedirect(reverse('ext:agent-manage'))
    return render(
        request, 'extension/agent-edit.html',
        {'ext_form': agent_form,'sipext': sipext})

@login_required
@has_role_decorator('admin')
def agent_create(request):
    agent_form = AgentsForm(
        request.POST or None)
    if agent_form.is_valid():
        agent = agent_form.save()
        create_agent();
        manager = connect_to_asterisk()
        try:
            channels = manager.Command("reload")
        except Exception as e:
            print(e)
        finally:
            manager.close()
        message = _('Your agent has been successfully created.')
        messages.success(request, message)
        return HttpResponseRedirect(reverse('ext:agent-manage'))
    return TemplateResponse(
        request, 'extension/agent-create.html',
        {'ext_form': agent_form})

@login_required
@has_role_decorator('admin')
def ext_manage(request):
    ext = ExtTable(SipExtension.objects.all())
    ext.paginate(page=request.GET.get('page', 1), per_page=25)
    return render(request, 'extension/ext-manage.html', {
        'ext': ext
    })

@login_required
@has_role_decorator('admin')
def agent_manage(request):
    agent = AgentTable(AgentConf.objects.all())
    agent.paginate(page=request.GET.get('page', 1), per_page=25)
    return render(request, 'extension/agent-manage.html', {
        'agent': agent
    })

def create_sip():
    try:
        os.remove("/etc/asterisk/sip_custom.conf")
    except OSError:
        pass

    with open("/etc/asterisk/sip_custom.conf", 'w') as ex_file:
        sipext = SipExtension.objects.all()
        for record in sipext:
            ex_file.write('[{}]\n'.format(record.username))
            ex_file.write('type = {}\n'.format(record.type))
            ex_file.write('callerid = {} <{}>\n'.format(record.name,record.extension))
            ex_file.write('defaultuser = {}\n'.format(record.username))
            ex_file.write('host = {}\n'.format(record.host))
            ex_file.write('secret = {}\n'.format(record.secret))
            ex_file.write('canreinvite = {}\n'.format(record.canreinvite))
            ex_file.write('insecure = {}\n'.format(record.insecure))
            ex_file.write('qualify = {}\n'.format(record.qualify))
            ex_file.write('nat = {}\n'.format(record.nat))
            ex_file.write('context = {}\n'.format(record.context))
            ex_file.write('bindport = {}\n'.format(record.bindport))
            ex_file.write('srvlookup = {}\n'.format(record.srvlookup))
            ex_file.write('disallow = {}\n'.format(record.disallow))
            msg_list = record.allow.split(',')
            for rst in msg_list:
                ex_file.write('allow = {}\n'.format(rst))
            ex_file.write('\n')
    ex_file.closed

def create_agent():
    try:
        os.remove("/etc/asterisk/agent_custom.conf")
    except OSError:
        pass

    with open("/etc/asterisk/agent_custom.conf", 'w') as ex_file:
        agent_r = AgentConf.objects.all()
        for record in agent_r:
            ex_file.write('agent = {},{},{} {}\n'.format(record.extension,record.extension_secret,
                                                         record.agent.first_name, record.agent.last_name))

    ex_file.closed


@login_required
@has_role_decorator('admin')
def agent_detail(request, pk):
    agent = get_object_or_404(AgentConf, pk=pk)
    agent_form = AgentForm(request.POST or None, instance=agent)

    return render(
        request, 'extension/agent-detail.html',
        {'ext_form': agent_form, 'agent': agent})

def hoax_create(request):
    hoax_form = HoaxSettingForm(
        request.POST or None)
    if hoax_form.is_valid():
        hoax_form.save()
        message = _('The hoax setting has been successfully created.')
        messages.success(request, message)
        return HttpResponseRedirect(reverse('ext:hoax-manage'))
    return TemplateResponse(
        request, 'extension/hoax-create.html',
        {'hoax_form': hoax_form})

def hoax_manage(request):
    hoax = HoaxSettingTable(HoaxSetting.objects.all())
    hoax.paginate(page=request.GET.get('page', 1), per_page=25)
    return render(request, 'extension/hoax-manage.html', {
        'hoax': hoax
    })

def hoax_edit(request, pk):
    hoax = get_object_or_404(HoaxSetting, pk=pk)
    hoax_form = HoaxSettingForm(request.POST or None, instance=hoax)
    if hoax_form.is_valid():
        hoax_form.save()
        message = _('Hoax information successfully updated.')
        messages.success(request, message)
        return HttpResponseRedirect(reverse('ext:hoax-manage'))
    return render(
        request, 'extension/hoax-edit.html',
        {'hoax_form': hoax_form})