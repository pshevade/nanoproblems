from django.shortcuts import render
from django.http import HttpResponse
from problems.models import Tag
from django.http import Http404
from django.http import HttpResponseRedirect
from django.core import serializers

from .models import Problem, Solution
import logic
from .forms import ProblemForm, SolutionForm
from users.logic import is_authenticated, is_authorized, is_admin, get_true_if_admin
from users.models import User

from comments.forms import CommentForm
from comments.models import Comment
import comments.logic as comments_logic

import problems
import json

import bleach
import markdown
from datetime import datetime


@is_authenticated()
def problems_list(request):
    """ List of all problems. """
    user = User.objects.get(email=request.session['email'])
    print "This is the signed in user we found: ", user.nickname, user.user_key
    latest_problems_list = Problem.objects.order_by('posted')[:10]
    for problem in latest_problems_list:
        problem.description = markdown.markdown(problem.description,
                                                extensions=['markdown.extensions.fenced_code'])
    context = {'latest_problems_list': latest_problems_list, 'user': user}
    return render(request, 'problems/problems_list.html', context)


@is_authenticated()
def problem_detail(request, problem_id):
    """ Return the problem details by problem_id. """
    context = logic.get_problem_details(request, problem_id)
    print context
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
            tag_objects_list = logic._get_tags(form.cleaned_data['tags_list'])
            for tag_object in tag_objects_list:
                problem.tags.add(tag_object)
            problem.save()
            # return HttpResponse(str(problem.id))
            return HttpResponseRedirect('/problems/')
        else:
            print "These are the problem errors! ", form.errors
            raise Http404("Form is not valid")
    else:
        # Remove when front end updated.
        form = ProblemForm()
    return render(request, 'problems/new_problem.html', {'form': form})


@is_admin()
@is_authenticated()
def mark_problem(request, problem_id):
    problem = logic.get_problem(problem_id)
    problem.marked = datetime.today()
    problem.save()
    return HttpResponseRedirect('/problems/' + str(problem_id))


@is_authenticated()
def vote_problem(request, problem_id, vote):
    print "Inside vote_problem for problem id: ", problem_id, "and vote: ", vote
    problem = logic.get_problem(problem_id)
    problem = logic.vote_on_problem(request, problem, vote)
    # return HttpResponseRedirect('/problems/' + str(problem_id))
    return HttpResponse(logic.get_problem_as_json(problem), content_type='application/json')


@is_authenticated()
def problem_as_json(request, problem_id):
    return HttpResponse(logic.get_problem_as_json(logic.get_problem(problem_id)),
                        content_type='application/json')


@is_admin()
@is_authenticated()
def problems_json(request):
    return HttpResponse(logic.get_problems_json(), content_type='application/json')


@is_authenticated()
def new_solution(request, problem_id):
    problem = logic.get_problem(problem_id)
    if request.method == "POST":
        solution_form = SolutionForm(request.POST)
        if solution_form.is_valid():
            # print "The users line is: ", submission_form['members_list']
            solution = solution_form.save(commit=False)
            solution.problem = problem
            user_profile = User.objects.get(email=request.session['email'])
            solution.user = user_profile
            solution.description = bleach.clean(solution.description, strip=True)
            solution.save()
            return HttpResponseRedirect('/problems/' + str(problem_id))
        else:
            raise Http404('Form is not valid')

    else:
        solution_form = SolutionForm()
        return render(request, 'problems/new_solution.html', {'form': solution_form, 'problem_id': problem_id})


@is_authenticated()
def edit_solution(request, problem_id, solution_id):
    print "inside edit_solution"
    solution = logic.get_solution(solution_id)
    if request.method == 'POST':
        print "inside post"
        logic.edit_solution(request, solution)
        return HttpResponseRedirect('/problems/' + str(problem_id) + '/show_solution/' + str(solution_id))
    else:
        form = SolutionForm()
        return render(request, 'problems/edit_solution.html', {'form': form, 'solution': solution, 'problem_id': problem_id})


@is_authenticated()
def delete_solution(request, problem_id, solution_id):
    print "inside edit_solution"
    solution = logic.get_solution(solution_id)
    if request.method == 'POST':
        print "inside post"
        logic.delete_solution(request, solution)
        return HttpResponseRedirect('/problems/' + str(problem_id))
    else:
        return render(request, 'problems/delete_solution.html', {'solution': solution, 'problem_id': problem_id})


@is_authenticated()
def show_solution(request, problem_id, solution_id):
    print "problem_id is: ", problem_id
    print "solution_id is: ", solution_id
    context = logic.get_solution_details(request, problem_id, solution_id)
    return render(request, 'problems/show_solution.html', context)


@is_authenticated()
def vote_solution(request, problem_id, solution_id, vote=0):
    solution = logic.get_solution(solution_id)
    solution = logic.vote_on_solution(request, solution, vote)
    return HttpResponse(logic.get_solution_as_json(solution), content_type='application/json')


@is_authenticated()
def solution_as_json(request, solution_id):
    return HttpResponse(logic.get_solution_as_json(logic.get_solution(solution_id)),
                        content_type='application/json')


@is_admin()
@is_authenticated()
def solutions_json(request):
    return HttpResponse(logic.get_solutions_json(), content_type='application/json')


@is_authenticated()
def add_comment_to_problem(request, problem_id):
    problem = logic.get_problem(problem_id)
    if request.method == 'POST':
        logic.new_comment_problem(request, problem)
    return HttpResponseRedirect('/problems/' + str(problem_id))


@is_authenticated()
def edit_comment_from_problem(request, problem_id, comment_id):
    problem = logic.get_problem(problem_id)
    comment = comments_logic.get_comment(comment_id)
    if request.method == 'POST':
        comment = logic.edit_comment_problem(request, problem, comment_id)
        return HttpResponseRedirect('/problems/' + str(problem_id))
    else:
        comment_form = CommentForm()
    return render(request, 'problems/edit_comment.html',
                  {'form': comment_form, 'problem_id': problem_id, 'comment':comment})


@is_authenticated()
def delete_comment_from_problem(request, problem_id, comment_id):
    print "inside delete_comment_from_problem"
    problem = Problem.objects.get(pk=problem_id)
    if request.method == 'GET':
        logic.delete_comment_problem(request, problem, comment_id)
    #return problem_detail(request, problem_id)
    return HttpResponseRedirect('/problems/' + str(problem_id))


@is_authenticated()
def add_comment_to_solution(request, problem_id, solution_id):
    print "inside add_comment_to_solution"
    solution = logic.get_solution(solution_id)
    if request.method == 'POST':
        print "request method is post!"
        logic.new_comment_solution(request, solution)
    print "sending to show_solution from add_comment_to_solution"
    return HttpResponseRedirect('/problems/' + str(problem_id) + '/show_solution/' + str(solution_id))


@is_authenticated()
def edit_comment_from_solution(request, problem_id, solution_id, comment_id):
    solution = logic.get_solution(solution_id)
    comment = comments_logic.get_comment(comment_id)
    if request.method == 'POST':
        comment = logic.edit_comment_solution(request, solution, comment_id)
        return HttpResponseRedirect('/problems/' + str(problem_id) + '/show_solution/' + str(solution_id))
    else:
        comment_form = CommentForm()
    return render(request, 'problems/edit_comment_solution.html',
                  {'form': comment_form, 'problem_id':problem_id, 'solution_id': solution_id, 'comment':comment})


@is_authenticated()
def delete_comment_from_solution(request, problem_id, solution_id, comment_id):
    solution = logic.get_solution(solution_id)
    if request.method == 'GET':
        logic.delete_comment_solution(request, solution, comment_id)
    return HttpResponseRedirect('/problems/' + str(problem_id) + '/show_solution/' + str(solution_id))
