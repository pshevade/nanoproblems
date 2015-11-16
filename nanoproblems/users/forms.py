from django import forms
from .models import User


class UserForm(forms.ModelForm):

    """ User Profile Form. """

    class Meta:
        model = User
        # don't want to change the email or the udacity key
        exclude = ('email',)
