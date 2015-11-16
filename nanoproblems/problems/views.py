from django.shortcuts import render
from django.http import HttpResponse
from problems.models import Tag
from django.http import Http404
from django.http import HttpResponseRedirect
from django.core import serializers

from .models import Problem, Solution
from .logic import _get_tags
from .forms import ProblemForm, SolutionForm
from users.views import is_authenticated
from users.models import User

from comments.forms import CommentForm
from comments.models import Comment

import problems
import json

import bleach
import markdown


@is_authenticated()
def problems_list(request):
    """ List of all problems. """
    user = User.objects.get(email=request.session['email'])
    print "This is the signed in user we found: ", user.nickname, user.user_key
    latest_problems_list = Problem.objects.order_by('posted')[:10]
    context = {'latest_problems_list': latest_problems_list, 'user': user}
    return render(request, 'problems/problems_list.html', context)


@is_authenticated()
def problem_detail(request, problem_id):
    """ Return the problem details by problem_id. """
    try:
        problem = Problem.objects.get(pk=problem_id)
        problem.description = markdown.markdown(problem.description, extensions=['markdown.extensions.fenced_code'])
        user = User.objects.get(email=request.session['email'])
        solutions_list = Solution.objects.filter(problem=problem)# need to add a way to get all answers to all questions here...
    except Problem.DoesNotExist:
        raise Http404("Project does not exist")
    context = {'problem': problem, 'user_email': request.session['email'], 'solutions_list':solutions_list}
    return render(request, 'problems/problem_detail.html', context)


@is_authenticated()
def new_problem(request):
    """ Create project from user input.

    GET: Return the form to create a project.
    POST: Create a new project and redirect to the project details
    """
    if request.method == "POST":
        # temp = json.loads(request.body)
        form = ProblemForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            problem = form.save(commit=False)
            # fint the user profile object based on the email in session
            user = User.objects.get(email=request.session['email'])
            problem.user = user
            problem.description = bleach.clean(problem.description, strip=True)
            # Save the project object - project needs to exist before
            # manytomany field is accessed.
            problem.save()
            # get the list of tag objects to add to project
            tag_objects_list = _get_tags(form.cleaned_data['tags_list'])
            for tag_object in tag_objects_list:
                problem.tags.add(tag_object)
            problem.save()
            # return HttpResponse(str(problem.id))
            return HttpResponseRedirect('/problems/')
        else:
            raise Http404("Form is not valid")
    else:
        # Remove when front end updated.
        form = ProblemForm()
    return render(request, 'problems/new_problem.html', {'form': form})


@is_authenticated()
def new_solution(request, problem_id):
    problem = Problem.objects.get(pk=problem_id)
    if request.method == "POST":
        solution_form = SolutionForm(request.POST)
        if solution_form.is_valid():
            # print "The users line is: ", submission_form['members_list']
            solution = solution_form.save(commit=False)
            solution.description = bleach.clean(solution.description, strip=True)
            solution.problem = problem
            user_profile = User.objects.get(email=request.session['email'])
            solution.user = user_profile
            solution.save()
            return HttpResponseRedirect('/problems/' + str(problem_id))
        else:
            raise Http404('Form is not valid')

    else:
        solution_form = SolutionForm()
        return render(request, 'problems/new_solution.html', {'form': solution_form, 'problem_id': problem_id})


# @is_authenticated()
# def add_new_comment(request, solution_id, problem_id):
#     solution = Solution.objects.get(pk=solution_id)
#     problem = Problem.objects.get(pk=problem_id)
#     if request.method == 'POST':
#         comment_form = CommentForm(request.POST)
#         if comment_form.is_valid():
#             comment = comment_form.save(commit=False)
#             comment.content = bleach.clean(comment.content, strip=True)
#             comment.user = User.objects.get(email=request.session['email'])
#             comment.save()
#             solution.comments.add(comment)
#         else:
#             raise Http404('Form is not valid')
#     problem.description = markdown.markdown(problem.description, extensions=['markdown.extensions.fenced_code'])
#     solution = Solution.objects.get(pk=solution_id)
#     comments_list = []
#     for comment in solution.comments.order_by('-posted'):
#         comment.content = markdown.markdown(comment.content, extensions=['markdown.extensions.fenced_code'])
#         comments_list.append(comment)
#     return HttpResponseRedirect('/problems/'+str(problem_id)+'/show_solution/'+str(solution_id))


@is_authenticated()
def show_solution(request, problem_id, solution_id):
    problem = Problem.objects.get(pk=problem_id)
    problem.description = markdown.markdown(problem.description, extensions=['markdown.extensions.fenced_code'])
    solution = Solution.objects.get(pk=solution_id)
    solution.description = markdown.markdown(solution.description, extransions=['markdown.extensions.fenced_code'])
    comments_list = []
    for comment in solution.comments.order_by('-posted'):
        comment.content = markdown.markdown(comment.content, extensions=['markdown.extensions.fenced_code'])
        comments_list.append(comment)
    context = {'solution': solution, 'problem': problem, 'user_email': request.session['email'], 'comments_list':comments_list}
    return render(request, 'problems/show_solution.html', context)


# @is_authenticated()
# def edit_comment(request, problem_id, solution_id, comment_id):
#     solution = Solution.objects.get(pk=solution_id)
#     try:
#         comment = Comment.objects.get(pk=comment_id)
#         if comment.user.email != request.session['email']:
#             return HttpResponseRedirect('/problems/'+str(problem_id)+'/show_solution/'+str(solution_id))
#     except Comment.DoesNotExist:
#         raise Http404("Comment does not exist")
#     if request.method == 'POST':
#         comment_form = CommentForm(request.POST, instance=comment)
#         if comment_form.is_valid():
#             comment = comment_form.save(commit=False)
#             comment.user = User.objects.get(email=request.session['email'])
#             comment.save()
#             solution.comments.add(comment)
#             return HttpResponseRedirect('/problems/'+str(problem_id)+'/show_solution/'+str(solution_id))
#         else:
#             print comment_form.errors
#     elif request.method == 'GET':
#         c_edit = comment
#         # c_edit.content = bleach.clean(c_edit.content, strip=True)
#         comment_form = CommentForm(instance=c_edit)

#         return render(request, 'problems/edit_comment.html',
#                       {'form': comment_form, 'problem_id': problem_id, 'solution_id': solution_id, 'comment':comment})


# @is_authenticated()
# def delete_comment(request, problem_id, solution_id, comment_id):
#     try:
#         solution = Solution.objects.get(pk=solution_id)
#         comment = Comment.objects.get(pk=comment_id)
#         if comment.user.email != request.session['email']:
#             return HttpResponseRedirect('/submissions/show/'+str(sub_id))
#         solution.comments.remove(comment)
#         comment.delete()

#     except Comment.DoesNotExist:
#         raise Http404("Comment does not exist")
#     return HttpResponseRedirect('/problems/'+str(problem_id)+'/show_solution/'+str(solution_id))


@is_authenticated()
def edit_problem(request, problem_id):
    pass
