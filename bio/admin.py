from django.contrib import admin
from .models import Biodata


admin.site.register(
    Biodata,
    list_display=["id", "name", "age","phone"],
)
