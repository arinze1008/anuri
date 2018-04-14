from django.contrib import admin

from .models import User,Profile,Callgroup,Agency,Roles

admin.site.register(Callgroup)
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Agency)
admin.site.register(Roles)