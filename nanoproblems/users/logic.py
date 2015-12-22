from django.shortcuts import render
from django.core.urlresolvers import reverse
from functools import wraps
# OpenID imports
from openid.consumer import consumer
# The standard openID formats to ask for user info, sreg is specific to openid provider
from openid.extensions import ax, sreg

from config import openid_settings
from django.http import Http404
from .models import User
from problems.models import Problem, Solution


def is_admin():
    """ Decorator to check if the user is an admin. """
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if 'email' in request.session:
                if '@knowlabs.com' in request.session['email'] or '@udacity.com' in request.session['email']:
                    return func(request, *args, **kwargs)
                else:
                    print "Not an admin!"
                    return False
        return wrapper
    return decorator


def is_authenticated():
    """ Decorator to check if user is authenticated """
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if 'email' in request.session:
                return func(request, *args, **kwargs)
            else:
                # find the namespace, convert to string
                namespace = func.__module__.split('.')[0]
                function_call = str(namespace + ':' + func.__name__)
                redirect = reverse(function_call, args=args, kwargs=kwargs)
                return render(request, 'users/login.html', {'redirect': redirect})
        return wrapper
    return decorator


def is_authorized():
    """ Decorator to check if the user is authorized
        for performing one action. """
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            print "the args: ", args
            print "the kwargs: ", kwargs
            for a in args:
                print a
                if 'user' in dir(a):
                    print "the argument is: ", a
                    user = a.__getattribute__('user')
                    print "the user object is: ", user
                    if user.email == request.session['email']:
                        return func(request, *args, **kwargs)
                    else:
                        print "not authorized for ", func.__name__
                else:
                    print "user not an attribute in any of the arguments."
        return wrapper
    return decorator


def get_user(request, user_key=None):
    if user_key:
        try:
            user = User.objects.get(user_key=user_key)
        except User.DoesNotExist:
            raise Http404("User doesnt exist")
    else:
        try:
            user = User.objects.get(email=request.session['email'])
        except User.DoesNotExist:
            raise Http404("User does not exist/is not signed in")
    return user


def get_user_submitted_problems(user):
    problems_list = Problem.objects.filter(user=user)
    return problems_list


def get_user_submitted_solutions(user):
    solutions_list = Solution.objects.filter(user=user)
    return solutions_list


def get_user_liked_problems(user):
    problems = Problem.objects.filter(like_vote_users=user).all()
    return problems


def get_user_liked_solutions(user):
    solutions = Solution.objects.filter(sol_like_vote_users=user).all()
    return solutions


def logout_user(request):
    """ log out a user - remove all info from session. """
    try:
        del request.session['email']
        del request.session['nickname']
    except KeyError:
        print "KeyError: User info not in session."


@is_admin()
def get_true_if_admin(request):
    return True


def get_udacity_openid_url(request):
    cons_obj = consumer.Consumer(request.session, None)
    openid_url = "https://www.udacity.com/openid"
    auth_request = cons_obj.begin(openid_url)

    # extending the reuqest object
    sreg_request = sreg.SRegRequest(
        required=['fullname', 'email', 'nickname'],
    )
    auth_request.addExtension(sreg_request)

    # To request for getting user_id @ udacity
    ax_request = ax.FetchRequest()
    # The url is associated with the user_id format at udacity
    ax_request.add(ax.AttrInfo('http://openid.net/schema/person/guid',
                               required=True,))

    auth_request.addExtension(ax_request)

    realm_url = openid_settings.REALM_URL
    return_url = openid_settings.RETURN_URL

    udacity_url = auth_request.redirectURL(realm_url, return_url)
    return udacity_url


def process_udacity_auth(request):
    """ Callback function for authentication with Udacity. """
    cons_obj = consumer.Consumer(request.session, None)
    path = openid_settings.RETURN_URL
    the_response = cons_obj.complete(request.GET, path)
    if the_response.status == consumer.SUCCESS:
        # Gather Info from Udacity
        sreg_response = sreg.SRegResponse.fromSuccessResponse(the_response)
        if sreg_response:
            sreg_items = {
                'email': sreg_response.get('email'),
                'name': sreg_response.get('nickname'),
            }
        ax_response = ax.FetchResponse.fromSuccessResponse(the_response)
        if ax_response:
            ax_items = {
                'udacity_key': ax_response.get('http://openid.net/schema/person/guid')[0],
            }
        # Store items returned from Udacity in the session object
        for key in sreg_items:
            request.session[key] = sreg_items[key]
        for key in ax_items:
            request.session[key] = ax_items[key]

    return request
