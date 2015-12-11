from django.forms import ModelForm
from .models import Problem, Solution
from django import forms


class ProblemForm(ModelForm):
    tags_list = forms.CharField()
    # articles_list = forms.CharField()

    class Meta:
        model = Problem
        exclude = ('user', 'tags', 'questions', 'comments', 'marked', 'likes', 'dislikes', 'like_vote_users', 'dislike_vote_users')


class SolutionForm(ModelForm):
    class Meta:
        model = Solution
        exclude = ('problem', 'user', 'comments', 'likes', 'dislikes', 'like_vote_users', 'dislike_vote_users')
