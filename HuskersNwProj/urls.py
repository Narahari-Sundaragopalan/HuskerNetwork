"""HuskersNwProj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.contrib.auth import views
from django.conf import settings
from django.conf.urls.static import static
from HuskersApp import views as app_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('HuskersApp.urls', namespace='HuskersApp')),
    url(r'^accounts/login/$', views.login, name='login', kwargs={'redirect_authenticated_user': True}),
    url(r'^accounts/logout/$', views.logout, name='logout', kwargs={'next_page': '/'}),
    url(r'^password_reset/$', views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', views.password_reset_complete, name='password_reset_complete'),
    url(r'^register/$', app_views.register, name='register'),
    #url('^oauth/', include('social_django.urls', namespace='social')),
    #url('^social-oauth/', include('social_django.urls', namespace='social')),
    url(r'^social-auth/', include('social.apps.django_app.urls', namespace='social')),
]


if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)