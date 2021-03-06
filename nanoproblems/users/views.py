from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import UserForm
from .models import User
from .models import NANODEGREE_CHOICES
import logic
from .logic import is_authenticated, logout_user, is_admin


def logout(request):
    """ Log the user out """
    # If the user was authenticated using Udacity
    logout_user(request)
    return HttpResponseRedirect('/problems/')


@is_authenticated()
def show(request, user_key):
    """ Show user's profile, and the project's they have created. """
    user = logic.get_user(request, user_key=user_key)
    problems = logic.get_user_submitted_problems(user)
    solutions = logic.get_user_submitted_solutions(user)
    liked_problems = logic.get_user_liked_problems(user)
    liked_solutions = logic.get_user_liked_solutions(user)
    return render(request,
                  'users/show_profile.html',
                  {'user': user,
                   'problems': problems,
                   'solutions': solutions,
                   'current_user': request.session['email'],
                   'liked_problems': liked_problems,
                   'liked_solutions': liked_solutions
                   })


@is_authenticated()
def edit(request):
    """ Edit the user's own profile """
    user = logic.get_user(request)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        # check whether it's valid:
        if form.is_valid():
            m = form.save()
            m.save()
            return HttpResponseRedirect('/users/show/' + str(user.user_key))
    else:
        return render(request, 'users/edit_profile.html',
                      {'form': UserForm(instance=user),
                       'user': user,
                       'nanodegree_choices': NANODEGREE_CHOICES})


def login(request):
    print "Inside login"
    """ Authenticate with Udacity using OpenID """
    if not hasattr(login, 'redirect_on_return'):
        login.redirect_on_return = '/problems/'
    if request.method == "POST":
        login.redirect_on_return = request.POST['redirect']
        udacity_url = logic.get_udacity_openid_url(request)
        return HttpResponseRedirect(udacity_url)
    elif request.method == "GET":
        request = logic.process_udacity_auth(request)

        if not User.objects.filter(email=request.session['email']).exists():
            user = User(email=request.session['email'],
                        nickname=request.session['name'])
            user.save()
        set_as_admin(request)
        return HttpResponseRedirect(login.redirect_on_return)


@is_admin()
def set_as_admin(request):
    user = User.objects.get(email=request.session['email'])
    print "Setting user to admin, email is: ", user.email
    user.is_admin = True
    user.save()
    return user
