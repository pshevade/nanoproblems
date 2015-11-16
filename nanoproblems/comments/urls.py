from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'new_comment/$', views.new_comment, name='new_comment'),
    url(r'^show_comment/(?P<comment_id>[0-9]+)$', views.show_comment, name='show_comment'),
    url(r'^edit_comment/(?P<comment_id>[0-9]+)$', views.edit_comment, name='edit_comment'),
    url(r'^delete_comment/(?P<comment_id>[0-9]+)$', views.delete_comment, name='delete_comment'),
    url(r'^comments_json/(?P<sub_id>[0-9]+)$', views.comments_json, name='comments_json'),
]
