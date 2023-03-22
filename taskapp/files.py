from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Task


# Create your forms here.

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    from django import forms
    from django.contrib.auth.forms import UserCreationForm

    class MyUserCreationForm(UserCreationForm):
        email = forms.EmailField()

        class Meta:
            model = User
            fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


# create a task
class CreateTask(forms.ModelForm):
    class Meta:
        model = Task
        field = ['title', 'content', ]
        exclude = ['user', ]
