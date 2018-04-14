from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from popup.models import AgentDispatch,Community
from django.db.models import Q
from django.contrib import messages
from django.utils.translation import ugettext as _
from .forms import DispatchForm,LocationContactForm
from django.http import Http404, HttpResponse
import json
from userprofile.models import Profile
from .models import Dispatch
from dal import autocomplete
from django.shortcuts import get_object_or_404
import datetime
from rolepermissions.decorators import has_role_decorator
# from rolepermissions.shortcuts import get_user_role
# Create your views here.

@login_required
# @has_role_decorator('dispatcher')
def view(request):
    dispatch_form = DispatchForm(
        request.POST or None)
    contact_form = LocationContactForm(request.GET or None)
    if dispatch_form.is_valid():

        dispatch_obj = dispatch_form.save(commit=False)
        dispatch_obj.user = request.user
        dispatch_obj.agency = request.user.profile.agency
        dispatch_obj.save()
        change_status(dispatch_form.cleaned_data['ticket_id'],dispatch_form.cleaned_data['status'])
        message = _('Note information successfully created.')
        messages.success(request, message)
        return HttpResponseRedirect(reverse('dispatcher:incidence'))
    user = request.user
    agency = user.profile.agency
    dispatch = Dispatch.objects.order_by('officer_reachout_time').reverse()
    dispatch = Dispatch.objects.filter(user=user).order_by('officer_reachout_time').reverse()
    incidence = AgentDispatch.objects.filter(status__in=['New','On-Going','Updated', 'On-Hold'],
                                             respondent=str(agency)).order_by('status')

    return render(
        request, 'dispatcher/dispatch_view.html',
        {'incidence': incidence,'dispatch_form': dispatch_form,'contact_form': contact_form,
         'dispatch': dispatch})

def change_status(id, status):
    dispatch_info = AgentDispatch.objects.get(id=int(id))
    if str(status) == "Dispatched":
        print datetime.datetime.now()
        dispatch_info.dispatch_time = datetime.datetime.now()
    dispatch_info.status = str(status)
    dispatch_info.save()


@login_required

def incidence_detail(request):
    if request.is_ajax():

        id = request.GET.get('id', None)
        dispatch_info = AgentDispatch.objects.get(id=id)
        dispatch_info.status = "On-Going"
        dispatch_info.save()
        data_info = {
            'Note': dispatch_info.note, 'Ticket ID': dispatch_info.ticket_id,
            'Emergency': dispatch_info.incidence,'status': dispatch_info.status,
            'Location': dispatch_info.location, 'Community': str(dispatch_info.community),
            'State': dispatch_info.state, 'Dispatch Time': str(dispatch_info.dispatch_time),

        }
        data = json.dumps(data_info)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404

@login_required

def dispatch_detail(request):
    if request.is_ajax():
        id = request.GET.get('id', None)
        dis_obj = get_object_or_404(Dispatch, pk=id)
        dispatch_info = AgentDispatch.objects.get(id=int(dis_obj.ticket_id))
        data_info = {
            'Note': dispatch_info.note, 'Ticket ID': dispatch_info.ticket_id,
            'Emergency': dispatch_info.incidence,'status': dispatch_info.status,
            'Location': dispatch_info.location, 'Community': str(dispatch_info.community),
            'State': dispatch_info.state, 'Dispatch Time': str(dispatch_info.dispatch_time),
            'Dispatcher Note':dis_obj.last_note

        }
        data = json.dumps(data_info)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404
class CommunityAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Community.objects.none()

        qs = Community.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs

def agency_incidence(request):
    agency_incidence = AgentDispatch.objects.filter(respondent=str(request.user.profile.agency.name)).order_by(
        'dispatch_time').reverse()
    return render(
        request, 'dispatcher/agency_incidence.html',
        {'agency_incidence': agency_incidence})

def agency_dispatch(request):
    agency_dispatch = Dispatch.objects.filter(agency=request.user.profile.agency).order_by('officer_reachout_time').reverse()

    return render(
        request, 'dispatcher/agency_dispatch.html',
        {'agency_dispatch': agency_dispatch})