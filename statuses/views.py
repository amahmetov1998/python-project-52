from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin


from .models import Status
from .forms import StatusForm
from .utils import NoPermissionMixin


class CreateStatus(NoPermissionMixin, SuccessMessageMixin, CreateView):
    form_class = StatusForm
    template_name = 'statuses/create_status.html'
    success_url = reverse_lazy('statuses')
    success_message = _('Status created successfully')


class ShowStatuses(NoPermissionMixin, ListView):
    template_name = 'statuses/statuses.html'
    context_object_name = 'statuses'
    model = Status


class UpdateStatus(NoPermissionMixin, SuccessMessageMixin, UpdateView):
    form_class = StatusForm
    model = Status
    template_name = 'statuses/update_status.html'
    success_url = reverse_lazy('statuses')
    success_message = _('Status changed successfully')


class DeleteStatus(NoPermissionMixin, DeleteView):
    model = Status
    context_object_name = 'status'
    template_name = 'statuses/delete_status.html'

    def form_valid(self, form):
        try:
            self.object.delete()
            messages.success(self.request, _("Status deleted successfully"))
            return redirect(reverse_lazy('statuses'))
        except ProtectedError:
            messages.error(self.request, _("The status cannot be deleted because it's used"))
            return redirect(reverse_lazy('statuses'))
