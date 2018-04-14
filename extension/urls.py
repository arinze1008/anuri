from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^extension/create/', views.ext_create, name='ext-create'),
    url(r'^extension/manage/$', views.ext_manage,
        name='ext-manage'),
    url(r'^extension/edit/(?P<pk>\d+)/$', views.ext_edit,
        name='ext-edit'),
    url(r'^extension/edit/$', views.ext_edit,
        name='ext-edit'),
    url(r'^extension/detail/(?P<pk>\d+)/$', views.ext_detail,
        name='ext-detail'),
    url(r'^extension/detail/$', views.ext_detail,
        name='ext-detail'),
    url(r'^agent/create/', views.agent_create, name='agent-create'),
    url(r'^agent/manage/$', views.agent_manage,
        name='agent-manage'),
    url(r'^agent/detail/(?P<pk>\d+)/$', views.agent_detail,
        name='agent-detail'),
    url(r'^agent/detail/$', views.agent_detail,
        name='agent-detail'),
    url(r'^agent/edit/(?P<pk>\d+)/$', views.agent_edit,
        name='agent-edit'),
    url(r'^agent/edit/$', views.agent_edit,
        name='agent-edit'),
    url(r'^hoax/create/', views.hoax_create, name='hoax-create'),
    url(r'^hoax/manage/$', views.hoax_manage,
        name='hoax-manage'),
    url(r'^hoax/edit/(?P<pk>\d+)/$', views.hoax_edit,
        name='hoax-edit'),
]

