# forms.py
from django import forms
from django.forms import ModelForm
from .models import Comment


class CommentForm(ModelForm):

    # content = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = Comment
        exclude = ('user', 'posted')
