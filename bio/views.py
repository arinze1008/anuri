from django.shortcuts import render
from .models import Biodata


def index(request):
    """
    Root page view. Just shows a list of values currently available.
    """
    return render(request, "bio/index.html", {
        "integer_values": Biodata.objects.order_by("id"),
    })
