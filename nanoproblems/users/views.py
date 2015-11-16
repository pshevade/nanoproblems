from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import Http404

from .forms import UserForm
from .models import User
from .models import NANODEGREE_CHOICES
from problems.models import Problem, Solution

from .logic import is_authenticated, logout_user, \
    get_udacity_openid_url, process_udacity_auth


def logout(request):
    """ Log the user out """
    # If the user was authenticated using Udacity
    logout_user(request)
    return HttpResponseRedirect('/problems/')


@is_authenticated()
def show(request, user_key):
    """ Show user's profile, and the project's they have created. """
    try:
        user = User.objects.get(user_key=user_key)
        problems_list = Problem.objects.filter(user=user)
        # Return all submissions that the user has made.
        solutions_list = Solution.objects.filter(user=user)
    except User.DoesNotExist:
        raise Http404("User doesnt exist")
    return render(request,
                  'users/show_profile.html',
                  {'user': user,
                   'problems': problems_list,
                   'solutions': solutions_list,
                   'current_user': request.session['email']}
                  )


@is_authenticated()
def edit(request):
    """ Edit the user's own profile """
    try:
        user = User.objects.get(email=request.session['email'])
    except User.DoesNotExist:
        raise Http404("User does not exist/is not signed in")
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        # check whether it's valid:
        if form.is_valid():
            m = form.save()
            m.save()
            return HttpResponseRedirect('/users/show/' + str(user.user_key))
    else:
        return render(request, 'users/edit_profile.html',
                      {'form': UserForm(instance=user), 'user': user, 'nanodegree_choices':NANODEGREE_CHOICES},)


def login(request):
    """ Authenticate with Udacity using OpenID """
    if not hasattr(login, 'redirect_on_return'):
        login.redirect_on_return = '/problems/'
    if request.method == "POST":
        login.redirect_on_return = request.POST['redirect']
        udacity_url = get_udacity_openid_url(request)
        return HttpResponseRedirect(udacity_url)
    elif request.method == "GET":
        request = process_udacity_auth(request)

        if not User.objects.filter(email=request.session['email']).exists():
            user = User(email=request.session['email'],
                        nickname=request.session['name'])
            user.save()
        else:
            pass
        return HttpResponseRedirect(login.redirect_on_return)
