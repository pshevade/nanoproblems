from users.logic import is_authorized
from .models import Tag, Problem, Solution
from .forms import SolutionForm
import comments.logic as comments_logic
import bleach
from django.http import Http404


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
    comments_list = []
    for comment in solution.comments.order_by('-posted'):
        comment.content = markdown.markdown(comment.content,
                                            extensions=['markdown.extensions.fenced_code'])
        comments_list.append(comment)
    print "this is the comments list: ", comments_list
    return {'solution': solution, 'problem': problem, 'user_email': request.session['email'], 'comments_list':comments_list}


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
