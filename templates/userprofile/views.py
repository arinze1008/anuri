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
from .models import Profile, User
from extension.models import Sync
from django.shortcuts import render
from userprofile.tables import UserTable
try:
    from Asterisk import Manager
except ImportError:
    Manager = None

@login_required
def details(request, pk):
    try:
        profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        profile = Profile(request.user)
    ctx = {'user': request.user, 'profile': profile}
    return TemplateResponse(request, 'userprofile/details.html', ctx)

@login_required
def profile_detail(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    profile_form = UserForm(request.POST or None, instance=profile)

    return render(
        request, 'userprofile/profile-detail.html',
        {'profile_form': profile_form, 'profile': profile})

@login_required
def profile_edit(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    profile_form = UpdateForm(request.POST or None, instance=profile)
    if profile_form.is_valid():
        if profile_form.cleaned_data['password'] != "":
            user = get_object_or_404(User, email=profile.user.email)
            user.set_password(profile_form.cleaned_data['password'])
            user.save()
        exten = profile_form.cleaned_data['extension']
        if exten == "":
            profile.extension = None
        profile_form.save()
        message = _('Profile information successfully updated.')
        messages.success(request, message)
        return HttpResponseRedirect(reverse('profile:user-manage'))
    return render(
        request, 'userprofile/profile-edit.html',
        {'profile_form': profile_form,'profile':profile})


@login_required
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
        profile.last_name = profile_form.cleaned_data['last_name']
        profile.first_name = profile_form.cleaned_data['first_name']
        profile.callgroup = profile_form.cleaned_data['callgroup']
        profile.phone = profile_form.cleaned_data['phone']
        profile.save()
        message = _('Your profile has been successfully created.')
        messages.success(request, message)
        return HttpResponseRedirect(reverse('profile:user-manage'))
    return TemplateResponse(
        request, 'userprofile/profile-create.html',
        {'profile_form': profile_form})

def user_manage(request):
    userprofile = UserTable(Profile.objects.all())
    userprofile.paginate(page=request.GET.get('page', 1), per_page=25)
    return render(request, 'userprofile/manage.html', {
        'userprofile': userprofile
    })

def agent_dashboard(request):
    user = request.user
    data = {'name': user.profile.first_name, 'extension': user.profile.extension}
    form = UserExForm(initial=data)

    print(form['extension'].value())
    if request.POST:
        manager = connect_to_asterisk()
        try:
            client_ip = request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ.get('REMOTE_ADDR')
            sync = Sync()
            sync.ip = client_ip
            print(client_ip)
            sync.ext = form['extension'].value()
            sync.save()
            manager.QueueAdd("tech_queue","SIP/{}".format(form['extension'].value()))
            return HttpResponseRedirect(reverse('profile:agent-logout'))
        except Exception as e:
            print(e)
        finally:
            manager.close()

    return render(request, 'userprofile/agent-dashboard.html', {
        'form': form
    })

def agent_logout(request):
    user = request.user
    if request.POST:
        manager = connect_to_asterisk()
        try:
            manager.QueueRemove("tech_queue","SIP/{}".format(user.profile.extension))
            # manager.QueueRemove("tech_queue", "SIP/105")
            return HttpResponseRedirect(reverse('profile:agent-dashboard'))
        except Exception as e:
            print(e)
        finally:
            manager.close()

    return render(request, 'userprofile/agent-logout.html', {
        'user': user
    })


def connect_to_asterisk():
    try:
        ast_manager = Manager.Manager(address=('localhost',5038), username='smartcall',secret= 'welcome')

    except Exception as e:
        print("Issues with connecting to asterisk server, {}".format(e))

    return ast_manager