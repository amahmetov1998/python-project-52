from django.forms import ModelForm
from django import forms
from .models import Status


class StatusForm(ModelForm):

    class Meta:
        model = Status
        fields = ('name',)
