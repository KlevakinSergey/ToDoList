from django import forms
from django.forms import ModelForm
from .models import Task
from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Добавить новое задание...'}))

    class Meta:
        model = Task
        fields = '__all__'


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username',  'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:

            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']