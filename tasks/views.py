from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.utils.translation import gettext as _
from django_filters.views import FilterView

from .filters import TaskFilter
from .forms import TaskForm
from .models import Task
from .utils import NoPermissionMixin


class CreateTask(NoPermissionMixin, SuccessMessageMixin, CreateView):
    form_class = TaskForm
    template_name = 'tasks/create_task.html'
    success_url = reverse_lazy('tasks')
    success_message = _('Task created successfully')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ShowTasks(NoPermissionMixin, FilterView):
    template_name = 'tasks/tasks.html'
    context_object_name = 'tasks'
    model = Task
    filterset_class = TaskFilter


class UpdateTask(NoPermissionMixin, SuccessMessageMixin, UpdateView):
    form_class = TaskForm
    model = Task
    template_name = 'tasks/update_task.html'
    success_url = reverse_lazy('tasks')
    success_message = _('Task changed successfully')


class DeleteTask(UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    template_name = 'tasks/delete_task.html'
    success_message = _('Task deleted successfully')
    success_url = reverse_lazy('tasks')

    def test_func(self):
        created_by_id = Task.objects.filter(
            id=self.kwargs['pk'])[0].created_by_id
        return self.request.user.id == created_by_id

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request,
                           _('The author can delete a task only'))
            return redirect(reverse_lazy('tasks'))
        else:
            messages.error(self.request,
                           _('You are not authorized! Please sign in.'))
            return redirect(reverse_lazy('login'))


class ViewTask(NoPermissionMixin, DetailView):
    model = Task
    template_name = 'tasks/view_task.html'
    context_object_name = 'task'
