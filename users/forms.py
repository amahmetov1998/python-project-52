from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')
    username = forms.CharField(
        label='Имя пользователя',
        help_text='Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.')
    password1 = forms.CharField(
        label='Пароль',
        help_text='Ваш пароль должен содержать как минимум 3 символа.',
        widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Подтверждение пароля',
        help_text='Для подтверждения введите, пожалуйста, пароль ещё раз.',
        widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class UpdateForm(RegisterForm):
    def clean_username(self):
        return self.cleaned_data.get('username')
