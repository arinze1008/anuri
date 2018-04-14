from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.details, name='details'),
    # url(r'^fees/$', views.fees, name='fees'),
    url(r'^profile/create/$', views.profile_create,
        name='profile-create'),
    url(r'^profile/user/$', views.user_manage,
        name='user-manage'),
    url(r'^profile/edit/(?P<pk>\d+)/$', views.profile_edit,
        name='profile-edit'),

]
