"""anuri URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from registration.urls import urlpatterns as registration_urls
from userprofile.urls import urlpatterns as userprofile_urls
from core.urls import urlpatterns as core_url
from extension.urls import urlpatterns as extension_urls
from popup.urls import urlpatterns as popup_urls
from report.urls import urlpatterns as report_urls
from dispatcher.urls import urlpatterns as dispatcher_urls
from popup.views import StateAutocompletes,CreateAutocomplete
from dispatcher.views import CommunityAutocomplete
from bio.urls import urlpatterns as bio_urls
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^', include(core_url)),
    url(r'^admin/', admin.site.urls),
    url(r'^account/', include(registration_urls, namespace='registration')),
    url(r'^profile/', include(userprofile_urls, namespace='profile')),
    url(r'^ext/', include(extension_urls, namespace='ext')),
    url(r'^popup/', include(popup_urls, namespace='popup')),
    url(r'^report/', include(report_urls, namespace='report')),
    url(r'^chaining/', include('smart_selects.urls')),
    # url(r'^select2/', include('django_select2.urls')),
    url(r'^dispatcher/', include(dispatcher_urls, namespace='dispatcher')),
    url(r'^bio/', include(bio_urls, namespace='bio')),

    url(
        r'^state-autocompletes/$',
        StateAutocompletes.as_view(),
        name='state-autocompletes',
    ),
     url(
        r'^create-autocomplete/$',
        CreateAutocomplete.as_view(create_field='name'),
        name='create-autocomplete',
    ),
    url(
        r'^community-autocomplete/$',
        CommunityAutocomplete.as_view(create_field='name'),
        name='community-autocomplete',
    ),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
