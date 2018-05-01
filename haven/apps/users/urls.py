from django.conf.urls import url 
from . import views 

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^login/process$', views.process_login),
    url(r'^register/process$', views.process_register),
    url(r'^users/community$', views.community),
    url(r'^users/(?P<id>\d+)$', views.users),
    url(r'^users/update_password$', views.update_password),
    url(r'^users/update_email$', views.update_email),
    url(r'^users/(?P<id>\d+)/settings$', views.settings),
    url(r'^logout$', views.logout)
]