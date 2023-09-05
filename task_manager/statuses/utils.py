from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic.base import View


class NoPermissionMixin(LoginRequiredMixin, View):

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request,
                           _('You are not authorized! Please sign in.'))
            return redirect(reverse_lazy('login'))
