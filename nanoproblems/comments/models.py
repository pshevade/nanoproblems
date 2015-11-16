""" Models for projects - project, tags. """

from django.db import models
from users.models import User


class Comment(models.Model):

    """ Comment class - all information in a comment. """

    content = models.TextField()
    posted = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, default=None)
    # submission = models.ForeignKey(Submission, default=None)

    def __unicode__(self):
        """ Return the url """
        return str(self.posted) + ' by ' + self.user.nickname


class Question(Comment):

    resolved = models.BooleanField()


class Answer(Comment):

    """ Answer to a particular question. """

    question = models.ForeignKey(Question, default=None)
