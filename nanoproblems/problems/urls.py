from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.problems_list, name='problems_list'),
    url(r'^(?P<problem_id>[0-9]+)/$', views.problem_detail, name='problem_detail'),
    # url(r'^(?P<problem_id>[0-9]+)/edit_problem', views.edit_problem, name='edit_problem'),
    url(r'new_problem/$', views.new_problem, name='new_problem'),
    url(r'^(?P<problem_id>[0-9]+)/mark_problem/$', views.mark_problem, name='mark_problem'),
    url(r'problems_json/$', views.problems_json, name='problems_json'),
    # url(r'^(?P<problem_id>[0-9]+)/delete_problem', views.delete_problem, name='delete_problem'),
    url(r'^(?P<problem_id>[0-9]+)/edit_comment/(?P<comment_id>[0-9]+)$', views.edit_comment_from_problem, name='edit_comment_from_problem'),
    url(r'^(?P<problem_id>[0-9]+)/delete_comment/(?P<comment_id>[0-9]+)$', views.delete_comment_from_problem, name='delete_comment_from_problem'),
    url(r'^(?P<problem_id>[0-9]+)/add_new_comment', views.add_comment_to_problem, name='add_comment_to_problem'),
    url(r'^(?P<problem_id>[0-9]+)/new_solution', views.new_solution, name='new_solution'),
    url(r'^(?P<problem_id>[0-9]+)/edit_solution/(?P<solution_id>[0-9]+)$', views.edit_solution, name='edit_solution'),
    url(r'^(?P<problem_id>[0-9]+)/delete_solution/(?P<solution_id>[0-9]+)$', views.delete_solution, name='delete_solution'),
    url(r'^(?P<problem_id>[0-9]+)/show_solution/(?P<solution_id>[0-9]+)/edit_comment/(?P<comment_id>[0-9]+)$', views.edit_comment_from_solution, name='edit_comment_from_solution'),
    url(r'^(?P<problem_id>[0-9]+)/show_solution/(?P<solution_id>[0-9]+)/delete_comment/(?P<comment_id>[0-9]+)$', views.delete_comment_from_solution, name='delete_comment_from_solution'),
    url(r'^(?P<problem_id>[0-9]+)/show_solution/(?P<solution_id>[0-9]+)/add_new_comment/', views.add_comment_to_solution, name='add_comment_to_solution'),
    url(r'^(?P<problem_id>[0-9]+)/show_solution/(?P<solution_id>[0-9]+)', views.show_solution, name='show_solution'),

    # url(r'^problems_JSON/$', views.problems_JSON, name='problems_JSON'),
    # url(r'^query_problems/$', views.query_problems, name='query_problems'),
]
#urls.py
