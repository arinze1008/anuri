from django.contrib import admin
from .models import Status,Resolved,Reason,Dispatch
# Register your models here.

admin.site.register(Status)
admin.site.register(Resolved)
admin.site.register(Reason)
admin.site.register(Dispatch)

