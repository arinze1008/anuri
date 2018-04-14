from django.conf.urls import url
from . import views
from popup.views import AgentbreakCreateView, NotifyList, LoginList, LogoutList,EndcallList

urlpatterns = [
    url(r'^console/(?P<pk>\d+)/$', views.home, name='console'),
    url(r'^console/$', views.home, name='console'),
    url(r'^agents/', views.available_agent, name='agents'),
    url(r'^packed_call/', views.packed_call, name='packed-call'),
    url(r'^supervisor/', views.supervisor, name='supervisor'),
    url(r'^queue_call/', views.queue_call, name='queue-call'),
    url(r'^live_call/', views.live_call, name='live-call'),
    url(r'^calling_call/', views.calling_call, name='calling-call'),
    url(r'^popup/create/', views.popup_create, name='popup-create'),
    url(r'^break/', AgentbreakCreateView.as_view(), name='agent-break'),
    url(r'^transfer/', views.transfer_agent, name='agent-transfer'),
    url(r'^call_transfer/(?P<channels>\w+)/$', views.transfer, name='call_transfer'),
    # url(r'^call_transfer/', views.transfer, name='call_transfer'),
    url(r'^spy/', views.myspy, name='spy'),
    url(r'^whisper/', views.whisper, name='whisper'),
    url(r'^barge/', views.barge, name='barge'),
    url(r'^hangup/', views.hangup, name='hangup'),
    url(r'^breaks/', views.breaks, name='breaks'),
    url(r'^end_break/', views.end_break, name='end-break'),
    url(r'^popup/edit/$', views.popup_edit,
        name='popup_edit'),
    url(r'^popup/edit/(?P<pk>\d+)/$', views.popup_edit,
        name='popup_edit'),
    url(r'^notify/', NotifyList.as_view(), name='notify'),
    url(r'^login/', LoginList.as_view(), name='login'),
    url(r'^logout/', LogoutList.as_view(), name='logout'),
    url(r'^endcall/', EndcallList.as_view(), name='endcall'),
    ]


