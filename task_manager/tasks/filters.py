import django_filters
from django import forms
from django_filters import ChoiceFilter, BooleanFilter
from django.utils.translation import gettext as _

from .models import Task
from task_manager.labels.models import Label


class TaskFilter(django_filters.FilterSet):
    label = ChoiceFilter(label=_('Label'),
                         choices=Label.objects.values_list('id', 'name')
                         )
    my_tasks = BooleanFilter(label=_('Only my tasks'),
                             widget=forms.CheckboxInput,
                             method='filter_tasks'
                             )

    class Meta:
        model = Task
        fields = ['status', 'executor']

    def filter_tasks(self, queryset, _, value):
        if value:
            return queryset.filter(created_by=self.request.user)
        return queryset
