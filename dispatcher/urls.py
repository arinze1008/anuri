from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^incidence/', views.view, name='incidence'),
    url(r'^incidence_detail/', views.incidence_detail, name='incidence_detail'),
    url(r'^dispatch_detail/', views.dispatch_detail, name='dispatch_detail'),
    url(r'^agency_dispatch/', views.agency_dispatch, name='agency_dispatch'),
    url(r'^agency_incidence/', views.agency_incidence, name='agency_incidence'),
    ]