from django.contrib import admin
from .models import AgentConf,HoaxDuration,Hoax,HoaxSetting
# Register your models here.

admin.site.register(AgentConf)
admin.site.register(HoaxDuration)
admin.site.register(Hoax)
admin.site.register(HoaxSetting)