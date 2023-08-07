from django import forms


class Form(forms.Form):
    content = forms.CharField(label='Текст')
