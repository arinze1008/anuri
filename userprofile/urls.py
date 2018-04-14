from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.details, name='details'),
    url(r'^profile/create/$', views.profile_create,
        name='profile-create'),
    url(r'^profile/user/$', views.user_manage,
        name='user-manage'),
    url(r'^agent/login/$', views.agent_dashboard,
        name='agent-dashboard'),
    url(r'^agent/logout/$', views.agent_logout,
        name='agent-logout'),
    url(r'^profile/edit/(?P<pk>\d+)/$', views.profile_edit,
        name='profile-edit'),
    url(r'^profile/edit/$', views.profile_edit,
        name='profile-edit'),
    url(r'^profile/detail/(?P<pk>\d+)/$', views.profile_detail,
        name='profile-detail'),
    url(r'^profile/detail/$', views.profile_detail,
        name='profile-detail'),
]
