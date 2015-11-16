""" urls.py for user_profile """
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^show/(?P<user_key>[\w.-]+)/$', views.show, name='show'),
    url(r'^edit/$', views.edit, name='edit'),
]
