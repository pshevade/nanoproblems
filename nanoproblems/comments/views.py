from django.shortcuts import render
from users.views import is_authenticated

from django.http import HttpResponseRedirect, HttpResponse


from .forms import CommentForm
from .models import Comment
import logic
from problems.models import Solution

from django.core import serializers

import json


# Create your views here.


@is_authenticated()
def new_comment(request):
    if request.method == "POST":
        comment = logic.new_comment(request)
        return HttpResponseRedirect('/comments/show_comment/' + str(comment.id))
    else:
        return render(request, 'comments/new_comment.html')


@is_authenticated()
def show_comment(request, comment_id):
    comment = logic.get_comment(comment_id)
    return render(request, 'comments/show_comment.html', {'comment':comment})


@is_authenticated()
def edit_comment(request, comment_id):
    comment = logic.get_comment(comment_id)
    if request.method == 'POST':
        print "going to edit comment by: ", comment.user.nickname
        logic.edit_comment(request, comment)
        return HttpResponseRedirect('/comments/show_comment/' + str(comment.id))
    elif request.method == 'GET':
        comment_form = CommentForm(instance=comment)
        return render(request, 'comments/edit_comment.html',
                      {'form': comment_form, 'comment': comment})


@is_authenticated()
def delete_comment(request, comment_id):
    comment = logic.get_comment(comment_id)
    if not logic.delete_comment(request, comment):
        return HttpResponseRedirect('/comments/show_comment/'+str(comment_id))
    return HttpResponseRedirect('/comments/show_comment/'+str(comment_id))


@is_authenticated()
def comments_json(request, sub_id):
    """ Return a list of projects with only a
        select list of fields (as set by the fields param)
    """
    solution = Solution.objects.get(pk=sub_id)
    comments_as_json = serializers.serialize(
        'json',
        solution.comments,
        fields=('user',
                'posted',
                'content',
                'description',
                'pk'),
        use_natural_foreign_keys=True)
    return HttpResponse(json.dumps(comments_as_json), content_type='json')

