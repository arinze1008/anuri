from django.db import models
from channels.binding.websockets import WebsocketBinding


class Biodata(models.Model):

    name = models.CharField(max_length=100, unique=True)
    age = models.IntegerField(default=0)
    phone = models.CharField(max_length=100, unique=True)


class BiodataBinding(WebsocketBinding):

    model = Biodata
    stream = "bioinfo"
    fields = ["name", "age"]

    @classmethod
    def group_names(cls, *args, **kwargs):
        return ["binding.values"]

    def has_permission(self, user, action, pk):
        return True
