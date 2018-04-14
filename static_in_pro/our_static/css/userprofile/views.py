from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist
from .forms import ProfileForm
from .models import Profile
from django.shortcuts import render
from userprofile.tables import UserTable

@login_required
def details(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        profile = Profile(request.user)
    ctx = {'user': request.user, 'profile': profile}
    return TemplateResponse(request, 'userprofile/details.html', ctx)


# @login_required
# def fees(request):
#     ctx = {'orders': request.user.fees.prefetch_related('groups__items')}
#     return TemplateResponse(request, 'userprofile/orders.html', ctx)


@login_required
def profile_edit(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    profile_form = ProfileForm(request.POST or None, instance=profile)
    if profile_form.is_valid():
        profile_form.save()
        message = _('Profile information successfully updated.')
        messages.success(request, message)
        return HttpResponseRedirect(reverse('profile:details'))
    return render(
        request, 'userprofile/profile-edit.html',
        {'profile_form': profile_form})


@login_required
def profile_create(request):
    user = request.user
    profile_form = ProfileForm(
        request.POST or None)
    profile_form.fields["user"].initial = user
    if profile_form.is_valid():
        profile = profile_form.save()
        user.profile = profile
        user.save()
        message = _('Your profile has been successfully created.')
        messages.success(request, message)
        return HttpResponseRedirect(reverse('profile:details'))
    return TemplateResponse(
        request, 'userprofile/manage.html',
        {'profile_form': profile_form, 'user':user})


@login_required
def user_manage(request):
    table = UserTable(Profile.objects.all())

    return render(request, 'userprofile/manage.html', {
        'table': table
    })

