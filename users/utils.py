from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy


class DataMixin(UserPassesTestMixin):
    login_url = reverse_lazy('users')

    def test_func(self):
        return self.request.user.id == self.kwargs['pk']
