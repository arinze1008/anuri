from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist
from .forms import ProfileForm,UserForm,UpdateForm,UserExForm
from .models import Profile, User, AgentSession
from django.conf import settings
from django.shortcuts import render
from userprofile.tables import UserTable
from report.models import Queue
try:
    from Asterisk import Manager
except ImportError:
    Manager = None
from rolepermissions.shortcuts import assign_role
from rolepermissions.verifications import has_role
from core.roles import Admin,Agent,Supervisor,Dispatcher
from rolepermissions.decorators import has_role_decorator
from rolepermissions.decorators import has_permission_decorator
from rolepermissions.shortcuts import grant_permission
from extension.models import AgentConf
from datetime import datetime

@login_required
def details(request):
    try:
        user = request.user
        if has_role(user, Agent):
            return HttpResponseRedirect(reverse('profile:agent-dashboard'))
        elif has_role(user, Admin):
            return HttpResponseRedirect(reverse('home'))
        elif has_role(user, Supervisor):
            return HttpResponseRedirect(reverse('home'))
        elif has_role(user,Dispatcher):
            return HttpResponseRedirect(reverse('dispatcher:incidence'))
    except ObjectDoesNotExist:
        pass
    # return redirect(settings.LOGIN_REDIRECT_URL)
    return HttpResponseRedirect(reverse('dispatcher:incidence'))


@login_required
@has_role_decorator('admin')
def profile_detail(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    profile_form = UserForm(request.POST or None, instance=profile)

    return render(
        request, 'userprofile/profile-detail.html',
        {'profile_form': profile_form, 'profile': profile})

@login_required
@has_role_decorator('admin')
def profile_edit(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    profile_form = UpdateForm(request.POST or None, instance=profile)
    if profile_form.is_valid():
        if profile_form.cleaned_data['password'] != "":
            user = get_object_or_404(User, email=profile.user.email)
            user.set_password(profile_form.cleaned_data['password'])
            user.save()
            myrole = profile_form.cleaned_data['role']
            str_role = str(myrole).lower()
            assign_role(user, str_role)
            if str_role == 'agent' or str_role == 'supervisor':
                grant_permission(user, 'view_call_console')
                grant_permission(user, 'create_call_record')
                grant_permission(user, 'edit_call_record')
                grant_permission(user, 'login_call_console')
                grant_permission(user, 'logout_call_console')
        profile.role = myrole

        profile_form.save()
        message = _('Profile information successfully updated.')
        messages.success(request, message)
        return HttpResponseRedirect(reverse('profile:user-manage'))
    return render(
        request, 'userprofile/profile-edit.html',
        {'profile_form': profile_form,'profile':profile})


@login_required
@has_role_decorator('admin')
def profile_create(request):
    profile_form = ProfileForm(
        request.POST or None)
    if profile_form.is_valid():
        user = User.objects.create_user(profile_form.cleaned_data['username'],
                                        profile_form.cleaned_data['password'],is_staff=True)
        profile = Profile()
        profile.user = user
        exten = profile_form.cleaned_data['extension']
        if exten == "":
            profile.extension = None
        else:
            profile.extension = exten
        profile.last_name = profile_form.cleaned_data['last_name']
        profile.first_name = profile_form.cleaned_data['first_name']
        profile.callgroup = profile_form.cleaned_data['callgroup']
        profile.phone = profile_form.cleaned_data['phone']
        agent = profile_form.cleaned_data['agency']
        if agent == "":
            profile.agency = None
        else:
            profile.agency = agent
        myrole = profile_form.cleaned_data['role']
        profile.role = myrole
        profile.save()
        # Assign role to the user
        assign_role(user, str(myrole).lower())
        message = _('Your profile has been successfully created.')
        messages.success(request, message)
        return HttpResponseRedirect(reverse('profile:user-manage'))
    return TemplateResponse(
        request, 'userprofile/profile-create.html',
        {'profile_form': profile_form})

@has_role_decorator('admin')
def user_manage(request):
    userprofile = UserTable(Profile.objects.all())
    userprofile.paginate(page=request.GET.get('page', 1), per_page=25)
    return render(request, 'userprofile/manage.html', {
        'userprofile': userprofile
    })

@has_permission_decorator('login_call_console')
def agent_dashboard(request):
    user = request.user
    try:
        user_agent = AgentConf.objects.get(agent=user.profile)
    except:
        user_agent = AgentConf()
    my_agent = user_agent.extension
    if request.POST:
        form = UserExForm(
            request.POST or None)
        ext = form['extension'].value()
        username = form['name'].value()
        manager = connect_to_asterisk()
        print ext
        try:

            manager.DBPut("agent", ext, username)
            monitor = manager.Originate('SIP/{}'.format(ext),
                                        context='login',
                                        extension = '{}'.format(ext),
                                        priority=1,
                                        async='yes')

            manager.QueueAdd("tech_queue", "Agent/{}".format(username))

            # return HttpResponseRedirect(reverse('popup:console',kwargs={'pk': int(my_agent)}))
        except Exception as e:
            print e
            # return HttpResponseRedirect(reverse('popup:console',kwargs={'pk': int(my_agent)}))
        finally:
            pass

        try:
            manager.QueuePause("tech_queue", "Agent/{}".format(my_agent), False)
        except Exception as e:
            print e
        finally:
            manager.close()
    data = {'name': user_agent.extension}
    form = UserExForm(initial=data)
    return render(request, 'userprofile/agent-dashboard.html', {
        'form': form,"my_agent":my_agent
    })

@has_permission_decorator('logout_call_console')
def agent_logout(request):
    user = request.user
    user_agent = AgentConf.objects.get(agent=user.profile)
    manager = connect_to_asterisk()
    try:
        my_agent = "Agent/{}".format(user_agent.extension)
        # queue_login = Queue.objects.filter(agent=my_agent,event="AGENTLOGIN").last()
        # diff = datetime.now() - queue_login.time
        manager.QueueRemove("tech_queue",my_agent)
        # AgentSession.objects.create(agent=user.profile,session_time=diff)
        return HttpResponseRedirect(reverse('profile:agent-dashboard'))
    except Exception as e:
        print(e)
    finally:
        manager.close()
    return HttpResponseRedirect(reverse('profile:agent-dashboard'))


def connect_to_asterisk():
    try:
        ast_manager = Manager.Manager(address=('localhost',5038), username='smartcall',secret= 'welcome')

    except Exception as e:
        print("Issues with connecting to asterisk server, {}".format(e))

    return ast_manager