from channels.generic.websockets import WebsocketDemultiplexer

from .models import AgentDispatchBinding, NotifyBinding, PopBinding, LoginBinding, LogoutBinding


class Demultiplexer(WebsocketDemultiplexer):
    consumers = {
        "incinfo": AgentDispatchBinding.consumer,
    }

    groups = ["binding.values"]


class Nomultiplexer(WebsocketDemultiplexer):
    consumers = {
        "supinfo":NotifyBinding.consumer
    }
    groups = ["bind.values"]

class Popmultiplexer(WebsocketDemultiplexer):
    consumers = {
        "popinfo":PopBinding.consumer,
    }
    groups = ["pop.values","logout.values"]

class Loginmultiplexer(WebsocketDemultiplexer):
    consumers = {
        "logininfo":LoginBinding.consumer,

    }
    groups = ["login.values"]

# class Logoutmultiplexer(WebsocketDemultiplexer):
#     consumers = {
#         # "logoutinfo":LogoutBinding.consumer
#     }
#     groups = ["logout.values","pop.values"]