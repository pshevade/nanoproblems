from django.db import models

from users.models import User
from comments.models import Question, Comment
# Create your models here.

CATEGORY_CHOICES = [('INTERVIEW', 'Interview Problem'),
                    ('CHALLENGE', 'Challenge Problem'),
                    ('QUESTION', 'The "I-have-a" Problem'),
                    ('CONTEST', 'Contest')]

DIFFICULTY_LEVEL = [('EASY', 'Easy'),
                    ('MEDIUM', 'Medium'),
                    ('HARD', 'Hard')]


class Tag(models.Model):

    """ Projects are tagged for classification. """
    tag_name = models.CharField(max_length=200)

    def __unicode__(self):
        """ Return the tag name to better identify object. """
        return self.tag_name

    def natural_key(self):
        return (self.tag_name)


class Problem(models.Model):

    """ Problem model to hold the information about a problem. """
    user = models.ForeignKey(User, default=None)
    title = models.CharField(max_length=200)
    description = models.TextField()
    posted = models.DateField(auto_now_add=True)

    category = models.CharField(max_length=15,
                                choices=CATEGORY_CHOICES,
                                default='CHALLENGE')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_LEVEL, default=1)
    # due_date = models.DateTimeField(default=None)
    tags = models.ManyToManyField(Tag)
    # questions = models.ManyToManyField(Question)
    comments = models.ManyToManyField(Comment)
    # marked is a date, when a problem is 'marked', we set the date to that date
    # and the problem appears on featured list for a week after.
    marked = models.DateField(default=None, null=True)


class Solution(models.Model):

    user = models.ForeignKey(User, default=None)
    title = models.CharField(max_length=200, default=None)
    problem = models.ForeignKey(Problem, default=None)
    description = models.TextField()
    posted = models.DateField(auto_now_add=True)
    comments = models.ManyToManyField(Comment)
