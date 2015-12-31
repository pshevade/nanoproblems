from django.http import Http404
from users.logic import is_authorized
from .models import Comment
from users.models import User
from .forms import CommentForm
import bleach
import json


def new_comment(request):
    """ Create a comment based on request form.
        Return comment if successful.
        Redirect to errors if failture.
    """
    user = User.objects.get(email=request.session['email'])
    print "In new_comment - request is still ajax? ", request.is_ajax()
    if request.is_ajax():
        if request.method == 'POST':
            print "Going to create comment."
            comment = Comment()
            print "Created an empty comment."
            comment.content = json.loads(request.body)['content']
            comment.user = user
            comment.save()
    else:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = user
            # Sanitize comment content before saving.
            comment.content = bleach.clean(comment.content, strip=True)
            comment.save()
        else:
            print comment_form.errors
            # Redirect to form errors in debug
            comment = False
    return comment


# @is_authorized()
def delete_comment(request, comment):
    """ Delete a given comment.
        Return False if not authorized.
    """
    try:
        comment.delete()
        return True
    except Exception:
        return False


# @is_authorized()
def edit_comment(request, comment):
    """ Edit a given comment.
        Return False if not authorized or if form errors.
    """
    print "inside editcomment"
    comment_form = CommentForm(request.POST, instance=comment)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.save()
        return True
    else:
        print comment_form.errors
        return False


def get_comment(comment_id):
    """ Check if a comment exists, raise 404 if not found. """
    try:
        comment = Comment.objects.get(pk=comment_id)
        return comment
    except Comment.DoesNotExist:
        raise Http404("Comment does not exist")
