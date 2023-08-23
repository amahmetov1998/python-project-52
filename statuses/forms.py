from django.forms import ModelForm
from django import forms
from .models import Status


class StatusForm(ModelForm):
    name = forms.CharField(label='Имя')

    class Meta:
        model = Status
        fields = ('name',)
