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


class DeleteStatus(NoPermissionMixin, SuccessMessageMixin, DeleteView):
    model = Status
    context_object_name = 'status'
    template_name = 'statuses/delete_status.html'
    success_message = _('Status deleted successfully')
    success_url = reverse_lazy('statuses')
