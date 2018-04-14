from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from rolepermissions.shortcuts import assign_role
from rolepermissions.verifications import has_role
from core.roles import Admin,Agent,Supervisor,Dispatcher
from rolepermissions.verifications import has_permission
from rolepermissions.shortcuts import available_perm_status
def home(request):
    user = request.user
    if user.is_authenticated:

        if has_role(user, Agent):
            return HttpResponseRedirect(reverse('profile:agent-dashboard'))
        elif has_role(user, Admin):
            return HttpResponseRedirect(reverse('home'))
        elif has_role(user, Supervisor):
            return TemplateResponse(request,'dashboard/welcome.html', {'product': None})
        elif has_role(user, Dispatcher):
            return HttpResponseRedirect(reverse('dispatcher:incidence'))
    return HttpResponseRedirect(reverse('registration:login'))



