from django.db import models
from statuses.models import Status
from labels.models import Label
from django.contrib.auth.models import User
from django.utils.translation import gettext as _


class Task(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name=_('Name'))
    description = models.TextField(verbose_name=_('Description'))
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name=_('Status'))
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created')
    executor = models.ForeignKey(User, on_delete=models.PROTECT,
                                 related_name='executor_task_set', blank=True, null=True, verbose_name=_('Executor'))
    label = models.ManyToManyField(Label, through='RelatedModel',
                                   through_fields=('task', 'label'), verbose_name=_('Label'), blank=True)


class RelatedModel(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)
