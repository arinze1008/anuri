from channels import route_class
from popup.consumers import Demultiplexer, Nomultiplexer,Popmultiplexer,Loginmultiplexer
    # Logoutmultiplexer


# The channel routing defines what channels get handled by what consumers,
# including optional matching on message attributes. In this example, we route
# all WebSocket connections to the class-based BindingConsumer (the consumer
# class itself specifies what channels it wants to consume)
channel_routing = [
    route_class(Demultiplexer, path='^/dispatcher/incidence/stream/?$'),
    route_class(Nomultiplexer, path='^/popup/supervisor/stream/?$'),
    route_class(Popmultiplexer, path='^/popup/console/(?P<pk>\d+)/stream/?$'),
    # route_class(Logoutmultiplexer, path='^/popup/console/(?P<pk>\d+)/stream/?$'),
    route_class(Loginmultiplexer, path='^/profile/agent/login/stream/?$'),

]
