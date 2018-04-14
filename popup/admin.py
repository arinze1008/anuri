from django.contrib import admin
from .forms import ComplaintForm
# Register your models here.
from .models import Respondent, Emergency, Breaks, INumber, Geopolitical,State,Lga,Complaint,\
    AgentDispatch,Community,Contact, LocationContact, Notify, LoginLogout, Logout

class RespondentAdmin(admin.ModelAdmin):
    list_display = ("agency","emergency")



class ComplaintAdmin(admin.ModelAdmin):
    form = ComplaintForm

admin.site.register(Respondent, RespondentAdmin)
admin.site.register(Emergency)
admin.site.register(Breaks)
admin.site.register(INumber)
admin.site.register(Geopolitical)
admin.site.register(State)
admin.site.register(Lga)
admin.site.register(Community)
admin.site.register(AgentDispatch)
admin.site.register(Complaint,ComplaintAdmin)
admin.site.register(Contact)
admin.site.register(LocationContact)
admin.site.register(Notify)
admin.site.register(LoginLogout)
admin.site.register(Logout)