from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin


from .models import Label
from .forms import LabelForm
from .utils import NoPermissionMixin


class CreateLabel(NoPermissionMixin, SuccessMessageMixin, CreateView):
    form_class = LabelForm
    template_name = 'labels/create_label.html'
    success_url = reverse_lazy('labels')
    success_message = _('Label created successfully')


class ShowLabels(NoPermissionMixin, ListView):
    template_name = 'labels/labels.html'
    context_object_name = 'labels'
    model = Label


class UpdateLabel(NoPermissionMixin, SuccessMessageMixin, UpdateView):
    form_class = LabelForm
    model = Label
    template_name = 'labels/update_label.html'
    success_url = reverse_lazy('labels')
    success_message = _('Label changed successfully')


class DeleteLabel(NoPermissionMixin, DeleteView):
    model = Label
    context_object_name = 'label'
    template_name = 'labels/delete_label.html'

    def form_valid(self, form):
        try:
            self.object.delete()
            messages.success(self.request, _("Label deleted successfully"))
            return redirect(reverse_lazy('labels'))
        except ProtectedError:
            messages.error(self.request, _("The label cannot be deleted because it's used"))
            return redirect(reverse_lazy('labels'))
