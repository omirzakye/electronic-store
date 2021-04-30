from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *


class MyUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Account
        fields = ('email', 'username')


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Account
        fields = ('email', 'username')
