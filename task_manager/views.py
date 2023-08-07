from django.shortcuts import render
from task_manager.forms import Form
from django.views import View


class FormView(View):
    def get(self, request, *args, **kwargs):
        form = Form()
        return render(request, 'index.html', {'form': form})
