from django.db.models import ProtectedError
from django.shortcuts import redirect
from .forms import *
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.utils.translation import gettext as _
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages


class RegisterUser(SuccessMessageMixin, CreateView):
    form_class = RegisterForm
    template_name = 'users/register_user.html'
    success_url = reverse_lazy('login')
    success_message = _('User registered successfully')


class LoginUser(SuccessMessageMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'users/login_user.html'
    success_message = _('You are logged in')


class Main(TemplateView):
    template_name = 'main.html'


class ShowUsers(ListView):
    template_name = 'users/users.html'
    context_object_name = 'users'
    model = User


class UpdateUser(SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    form_class = UpdateForm
    model = User
    template_name = 'users/update_user.html'
    success_url = reverse_lazy('users')
    success_message = _('User changed successfully')

    def test_func(self):
        return self.request.user.id == self.kwargs['pk']

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, _('You do not have rights to change another user.'))
            return redirect(reverse_lazy('users'))
        else:
            messages.error(self.request, _('You are not authorized! Please sign in.'))
            return redirect(reverse_lazy('login'))


class DeleteUser(UserPassesTestMixin, DeleteView):
    model = User
    context_object_name = 'user'
    template_name = 'users/delete_user.html'

    def form_valid(self, form):
        try:
            self.object.delete()
            messages.success(self.request, _("User deleted successfully"))
            return redirect(reverse_lazy('users'))
        except ProtectedError:
            messages.error(self.request, _("The user cannot be deleted because it's used"))
            return redirect(reverse_lazy('users'))

    def test_func(self):
        return self.request.user.id == self.kwargs['pk']

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, _('You do not have rights to change another user.'))
            return redirect(reverse_lazy('users'))
        else:
            messages.error(self.request, _('You are not authorized! Please sign in.'))
            return redirect(reverse_lazy('login'))


class LogoutUser(LogoutView):
    next_page = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _('You are logged out'))
        return super().dispatch(request, *args, **kwargs)
