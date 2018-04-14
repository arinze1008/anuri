from django.contrib import admin

from .models import User,Profile,Callgroup

admin.site.register(Callgroup)
admin.site.register(User)
admin.site.register(Profile)