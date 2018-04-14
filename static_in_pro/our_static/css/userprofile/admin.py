from django.contrib import admin

from .models import User,Profile,Callgroup,Extension

admin.site.register(Callgroup)
admin.site.register(Extension)
admin.site.register(User)
admin.site.register(Profile)