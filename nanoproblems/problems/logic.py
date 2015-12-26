from users.logic import is_authorized, get_true_if_admin
from .models import Tag, Problem, Solution
from users.models import User
from .forms import SolutionForm
import comments.logic as comments_logic
import bleach
from django.http import Http404
from django.core import serializers
import json

import markdown


def _get_tags(tag_string):
    """ Take the string of tags, and convert into tags object
        If tags already exist, dont create.
        Return a list of tag objects to add to the project
    """
    print "inside get_tags, string is: ", tag_string
    tag_objects_list = []
    # remove all whitespaces
    tag_string_cleaned = tag_string.replace(" ", "")
    tokens = tag_string_cleaned.split(',')
    for tok in tokens:
        try:
            tag_object = Tag.objects.get(tag_name=tok)
        except Tag.DoesNotExist:
            tag_object = Tag(tag_name=tok)
            tag_object.save()
        if tag_object not in tag_objects_list:
            tag_objects_list.append(tag_object)
    return tag_objects_list


def get_solution_details(request, problem_id, solution_id):
    problem = get_problem(problem_id)
    solution = get_solution(solution_id)
    user = User.objects.get(email=request.session['email'])
    comments_list = []
    for comment in solution.comments.order_by('-posted'):
        comment.content = markdown.markdown(comment.content,
                                            extensions=['markdown.extensions.fenced_code'])
        comments_list.append(comment)
    print "this is the comments list: ", comments_list
    return {'solution': solution, 'problem': problem, 'user': user, 'comments_list':comments_list}


@is_authorized()
def edit_solution(request, solution):
    form = SolutionForm(request.POST, instance=solution)
    if form.is_valid():
        s = form.save(commit=False)
        s.description = bleach.clean(s.description, strip=True)
        s.save()
        return s
    else:
        return False


@is_authorized()
def delete_solution(request, solution):
    try:
        solution.delete()
        return True
    except Exception, e:
        print e
        return False


def get_solution(solution_id):
    try:
        solution = Solution.objects.get(pk=solution_id)
        solution.description = markdown.markdown(solution.description,
                                                 extensions=['markdown.extensions.fenced_code'])
        return solution
    except Solution.DoesNotExist:
        raise Http404("Solution does not exist")


def get_problem(problem_id):
    try:
        problem = Problem.objects.get(pk=problem_id)
        problem.description = markdown.markdown(problem.description,
                                                extensions=['markdown.extensions.fenced_code'])
        return problem
    except Problem.DoesNotExist:
        raise Http404("Project does not exist")
    return False


def vote_on_problem(request, problem, vote):

    try:
        user = User.objects.get(email=request.session['email'])
    except User.DoesNotExist:
        raise Http404("User does not exist")
    user_in_likes = Problem.objects.filter(like_vote_users__email=user.email)\
                                   .filter(id=problem.id)
    user_in_dislikes = Problem.objects.filter(dislike_vote_users__email=user.email)\
                                      .filter(id=problem.id)
    if not user_in_likes and not user_in_dislikes:
        # This is the first time the
        if vote == '1':
            problem.likes += 1
            problem.like_vote_users.add(user)
            problem.save()
        elif vote == '2':
            problem.dislikes += 1
            problem.dislike_vote_users.add(user)
            problem.save()
    elif user_in_likes and not user_in_dislikes and vote == '2':
        print "User: ", user.email, " is in the like list."
        problem.dislikes += 1
        problem.likes -= 1
        problem.like_vote_users.remove(user)
        problem.dislike_vote_users.add(user)
        problem.save()
    elif user_in_dislikes and not user_in_likes and vote == '1':
        print "User: ", user.email, " is in the dislike list."
        problem.likes += 1
        problem.dislikes -= 1
        problem.dislike_vote_users.remove(user)
        problem.like_vote_users.add(user)
        problem.save()
    return problem


def vote_on_solution(request, solution, vote):

    try:
        user = User.objects.get(email=request.session['email'])
    except User.DoesNotExist:
        raise Http404("User does not exist")
    user_in_likes = Solution.objects.filter(sol_like_vote_users__email=user.email)\
                                    .filter(id=solution.id)
    user_in_dislikes = Solution.objects.filter(sol_dislike_vote_users__email=user.email)\
                                       .filter(id=solution.id)
    if not user_in_likes and not user_in_dislikes:
        # This is the first time the
        if vote == '1':
            solution.likes += 1
            solution.sol_like_vote_users.add(user)
            solution.save()
        elif vote == '2':
            solution.dislikes += 1
            solution.sol_dislike_vote_users.add(user)
            solution.save()
    elif user_in_likes and not user_in_dislikes and vote == '2':
        print "User: ", user.email, " is in the like list."
        solution.dislikes += 1
        solution.likes -= 1
        solution.sol_like_vote_users.remove(user)
        solution.sol_dislike_vote_users.add(user)
        solution.save()
    elif user_in_dislikes and not user_in_likes and vote == '1':
        print "User: ", user.email, " is in the dislike list."
        solution.likes += 1
        solution.dislikes -= 1
        solution.sol_dislike_vote_users.remove(user)
        solution.sol_like_vote_users.add(user)
        solution.save()
    return solution


def get_problem_as_json(problem):
    if problem:
        problem.description = markdown.markdown(problem.description,
                                                extensions=['markdown.extensions.fenced_code'])
        problem_serialized = serializers.serialize('json',
                                                   [problem],
                                                   fields=('title',
                                                           'posted',
                                                           'difficulty',
                                                           'description',
                                                           'tags',
                                                           'likes',
                                                           'dislikes',
                                                           'user',
                                                           'pk'),
                                                   use_natural_foreign_keys=True)
        return json.dumps(problem_serialized)
    else:
        return None


def get_problems_json():
    problems = Problem.objects.all()
    for problem in problems:
        problem.description = markdown.markdown(problem.description,
                                                extensions=['markdown.extensions.fenced_code'])
    problems_serialized = serializers.serialize('json',
                                                problems,
                                                fields=('title',
                                                        'posted',
                                                        'difficulty',
                                                        'description',
                                                        'tags',
                                                        'likes',
                                                        'dislikes',
                                                        'user',
                                                        'pk'),
                                                use_natural_foreign_keys=True)
    return json.dumps(problems_serialized)


def get_problem_details(request, problem_id):
    problem = get_problem(problem_id)
    solutions_list = Solution.objects.filter(problem=problem)# need to add a way to get all answers to all questions here...
    comments_list = []
    print "The solutions list is: ", solutions_list
    for comment in problem.comments.order_by('-posted'):
        comment.content = markdown.markdown(comment.content, extensions=['markdown.extensions.fenced_code'])
        comments_list.append(comment)
    markable = get_true_if_admin(request)
    print "problem is marked on: ", problem.marked
    return {'problem': problem, 'user': User.objects.get(email=request.session['email']), 'solutions_list':solutions_list, 'comments_list': comments_list, 'markable':markable}


def new_comment_problem(request, problem):
    """ Add a comment to a given problem.
    """
    comment = comments_logic.new_comment(request)
    if comment:
        problem.comments.add(comment)
        return True
    else:
        print "something went wrong, couldn't create a new comment for problem."
        return False


@is_authorized()
def edit_comment_problem(request, problem, comment_id):
    """ Edit comment.
    """
    comment = comments_logic.get_comment(comment_id)
    # Return false if comment is not in this problem!
    if comment:
        if comment not in problem.comments.all():
            return False
        comments_logic.edit_comment(request, comment)
        return comment
    else:
        print "something went wrong, couldn't find comment"
        return False


@is_authorized()
def delete_comment_problem(request, problem, comment_id):
    print "inside logic deletecommentproblem"
    comment = comments_logic.get_comment(comment_id)
    if comment:
        if comment in problem.comments.all():
            problem.comments.remove(comment)
        else:
            return False
        comments_logic.delete_comment(request, comment)
        return True
    else:
        print "something went wrong, couldn't find comment"
        return False


def new_comment_solution(request, solution):
    comment = comments_logic.new_comment(request)
    if comment:
        print "adding comment to solution"
        solution.comments.add(comment)
        return True
    else:
        print "something went wrong, couldn't create a new comment for problem."
        return False


@is_authorized()
def edit_comment_solution(request, solution, comment_id):
    """ Edit comment.
    """
    comment = comments_logic.get_comment(comment_id)
    # Return false if comment is not in this problem!
    if comment:
        if comment not in solution.comments.all():
            return False
        comments_logic.edit_comment(request, comment)
        return comment
    else:
        print "something went wrong, couldn't find comment"
        return False


@is_authorized()
def delete_comment_solution(request, solution, comment_id):
    comment = comments_logic.get_comment(comment_id)
    if comment:
        if comment in solution.comments.all():
            solution.comments.remove(comment)
        else:
            return False
        comments_logic.delete_comment(request, comment)
        return True
    else:
        print "something went wrong, couldn't find comment"
        return False


def get_solution_as_json(solution):
    if solution:
        solution.description = markdown.markdown(solution.description,
                                                 extensions=['markdown.extensions.fenced_code'])
        solution_serialized = serializers.serialize('json',
                                                    [solution],
                                                    fields=('title',
                                                            'posted',
                                                            'description',
                                                            'likes',
                                                            'dislikes',
                                                            'user',
                                                            'pk'),
                                                    use_natural_foreign_keys=True)
        return json.dumps(solution_serialized)
    else:
        return None


def get_solutions_json():
    solutions = Solution.objects.all()
    for solution in solutions:
        solution.description = markdown.markdown(solution.description,
                                                 extensions=['markdown.extensions.fenced_code'])
    solutions_serialized = serializers.serialize('json',
                                                 solutions,
                                                 fields=('title',
                                                         'posted',
                                                         'description',
                                                         'likes',
                                                         'dislikes',
                                                         'user',
                                                         'pk'),
                                                 use_natural_foreign_keys=True)
    return json.dumps(solutions_serialized)


def get_comments_as_json(solution_id=None, problem_id=None):
    comments_list=[]
    if problem_id:
        comment_from = get_problem(problem_id)
    if solution_id:
        comment_from = get_solution(solution_id)
    for comment in comment_from.comments.order_by('-posted'):
        comment.content = markdown.markdown(comment.content, extensions=['markdown.extensions.fenced_code'])
        comments_list.append(comment)
    comments_serialized = serializers.serialize('json',
                                                comments_list,
                                                fields=('content',
                                                        'posted',
                                                        'user',
                                                        'pk'),
                                                use_natural_foreign_keys=True)
    return json.dumps(comments_serialized)
