from channels.generic.websockets import WebsocketDemultiplexer

from .models import BiodataBinding


class Demultiplexer(WebsocketDemultiplexer):
    consumers = {
        "bioinfo": BiodataBinding.consumer,
    }

    groups = ["binding.values"]
