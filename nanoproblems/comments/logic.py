from django.http import Http404
from users.logic import is_authorized
from .models import Comment
from users.models import User
from .forms import CommentForm
import bleach


def createcomment(request):
    """ Create a comment based on request form.
        Return comment if successful.
        Redirect to errors if failture.
    """
    user = User.objects.get(email=request.session['email'])
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.user = user
        # Sanitize comment content before saving.
        comment.content = bleach.clean(comment.content, strip=True)
        comment.save()
        return comment
    else:
        print comment_form.errors
        # Redirect to form errors in debug
        return False


@is_authorized()
def deletecomment(request, comment):
    """ Delete a given comment.
        Return False if not authorized.
    """
    try:
        comment.delete()
        return True
    except Exception:
        return False


@is_authorized()
def editcomment(request, comment):
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


def checkcommentexists(comment_id):
    """ Check if a comment exists, raise 404 if not found. """
    try:
        comment = Comment.objects.get(pk=comment_id)
        return comment
    except Comment.DoesNotExist:
        raise Http404("Comment does not exist")
