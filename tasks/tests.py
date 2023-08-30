from .models import Status
from tasks.models import Task, RelatedModel
from labels.models import Label
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User


class SetUpTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            first_name='John', last_name='Lennon',
            username='john_lennon',
        )
        self.user.set_password('gtJej43j95')
        self.user.save()

        self.client.login(
            username='john_lennon', password='gtJej43j95',
        )

        self.status = Status.objects.create(name='Status')
        self.status.save()

        self.label = Label.objects.create(name='Label')
        self.label.save()

        self.task = Task.objects.create(name='Task', description='Text', status=self.status, created_by=self.user)
        self.task.save()

        self.table = RelatedModel.objects.create(task=self.task, label=self.label)
        self.table.save()


class TaskCreateTestCase(SetUpTestCase):

    def test_create_task(self):

        response = self.client.post(reverse('create_task'), {'name': 'New_task', 'description': 'New_text', 'status': 1,
                                                             'created_by': 1})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Задача успешно создана')

    def test_create_task_if_not_logged_in(self):

        self.client.logout()
        response = self.client.get(reverse('create_task'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Вы не авторизованы! Пожалуйста, выполните вход.')

    def test_tasks_access_if_not_logged_in(self):

        self.client.logout()
        response = self.client.get(reverse('tasks'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Вы не авторизованы! Пожалуйста, выполните вход.')


class TaskUpdateTestCase(SetUpTestCase):
    def test_update_task(self):
        response = self.client.post(reverse('update_task', kwargs={'pk': 1}),
                                    {'name': 'Text',
                                     'description': 'change_text',
                                     'status': 1,
                                     'created_by': 1})

        self.assertRedirects(response, reverse('tasks'))
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Задача успешно изменена')

    def test_update_task_if_not_logged_in(self):

        self.client.logout()
        response = self.client.get(reverse('update_task', kwargs={'pk': 1}))

        self.assertRedirects(response, reverse('login'))
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Вы не авторизованы! Пожалуйста, выполните вход.')


class TaskDeleteTestCase(SetUpTestCase):
    def test_delete_task(self):

        response = self.client.post(reverse('delete_task', kwargs={'pk': 1}))

        self.assertRedirects(response, reverse('tasks'))
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Задача успешно удалена')

    def test_delete_task_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('delete_task', kwargs={'pk': 1}))

        self.assertRedirects(response, reverse('login'))
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Вы не авторизованы! Пожалуйста, выполните вход.')

    def test_delete_task_if_no_permission(self):
        self.client.logout()
        self.user = User.objects.create(
            first_name='Katy', last_name='Perry',
            username='katy_perry',
        )
        self.user.set_password('at1J5fe36we')
        self.user.save()

        self.client.login(
            username='katy_perry', password='at1J5fe36we',
        )
        response = self.client.get(reverse('delete_task', kwargs={'pk': 1}))

        self.assertRedirects(response, reverse('tasks'))
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Задачу может удалить только ее автор')


class ObjectsDeleteTestCase(SetUpTestCase):

    def test_delete_status_if_related(self):
        response = self.client.post(reverse('delete_status', kwargs={'pk': 1}))

        self.assertRedirects(response, reverse('statuses'))
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Невозможно удалить статус, потому что он используется')

    def test_delete_user_if_related(self):
        response = self.client.post(reverse('delete_user', kwargs={'pk': 1}))

        self.assertRedirects(response, reverse('users'))
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Невозможно удалить пользователя, потому что он используется')

    def test_delete_label_if_related(self):
        response = self.client.post(reverse('delete_label', kwargs={'pk': 1}))

        self.assertRedirects(response, reverse('labels'))
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Невозможно удалить метку, потому что она используется')
