from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import gettext as _


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label=_('Name'))
    last_name = forms.CharField(label=_('Surname'))
    username = forms.CharField(
        label=_('Username'),
        help_text=_('Required field. No more than 150 characters. Letters, numbers and symbols @/./+/-/_ only.'))
    password1 = forms.CharField(
        label=_('Password'),
        help_text=_('Your password must contain at least 3 characters.'),
        widget=forms.PasswordInput)
    password2 = forms.CharField(
        label=_('Password confirmation'),
        help_text=_('To confirm, please enter your password again.'),
        widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label=_('Username'))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput)


class UpdateForm(RegisterForm):
    def clean_username(self):
        return self.cleaned_data.get('username')
