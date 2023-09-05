from .models import Status
from task_manager.tasks.models import Task, RelatedModel
from task_manager.labels.models import Label
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

        self.user2 = User.objects.create(
            first_name='Katy', last_name='Perry',
            username='katy_perry',
        )
        self.user2.set_password('at1J5fe36we')
        self.user2.save()

        self.client.login(
            username='john_lennon', password='gtJej43j95',
        )

        self.status = Status.objects.create(name='Status')
        self.status.save()

        self.label1 = Label.objects.create(name='Label_1')
        self.label1.save()

        self.label2 = Label.objects.create(name='Label_2')
        self.label2.save()

        self.task1 = Task.objects.create(
            name='Task_1',
            description='Text_1',
            status=self.status,
            created_by=self.user,
            executor=self.user
        )
        self.task1.save()

        self.task2 = Task.objects.create(
            name='Task_2',
            description='Text_2',
            status=self.status,
            created_by=self.user,
            executor=self.user2
        )
        self.task2.save()

        self.task3 = Task.objects.create(
            name='Task_3',
            description='Text_3',
            status=self.status,
            created_by=self.user,
            executor=self.user2
        )
        self.task3.save()

        self.table1 = RelatedModel.objects.create(
            task=self.task1,
            label=self.label1
        )
        self.table1.save()

        self.table2 = RelatedModel.objects.create(
            task=self.task2,
            label=self.label2
        )
        self.table2.save()

        self.table3 = RelatedModel.objects.create(
            task=self.task3,
            label=self.label2
        )
        self.table3.save()


class TaskCreateTestCase(SetUpTestCase):

    def test_create_task(self):

        response = self.client.post(reverse('create_task'),
                                    {'name': 'New_task',
                                     'description': 'New_text',
                                     'status': 1,
                                     'executor': 1}
                                    )

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
        self.assertEqual(str(messages[0]),
                         'Вы не авторизованы! Пожалуйста, выполните вход.'
                         )

    def test_tasks_access_if_not_logged_in(self):

        self.client.logout()
        response = self.client.get(reverse('tasks'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Вы не авторизованы! Пожалуйста, выполните вход.'
        )


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
        self.assertEqual(str(messages[0]),
                         'Вы не авторизованы! Пожалуйста, выполните вход.')


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
        self.assertEqual(
            str(messages[0]),
            'Вы не авторизованы! Пожалуйста, выполните вход.'
        )

    def test_delete_task_if_no_permission(self):
        self.client.logout()
        self.user = User.objects.create(
            first_name='Bob', last_name='Marley',
            username='bob_marley',
        )
        self.user.set_password('34k33fkQkw')
        self.user.save()

        self.client.login(
            username='bob_marley', password='34k33fkQkw',
        )
        response = self.client.get(reverse('delete_task', kwargs={'pk': 1}))

        self.assertRedirects(response, reverse('tasks'))
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]),
                         'Задачу может удалить только ее автор')


class ObjectsDeleteTestCase(SetUpTestCase):

    def test_delete_status_if_related(self):
        response = self.client.post(reverse('delete_status', kwargs={'pk': 1}))

        self.assertRedirects(response, reverse('statuses'))
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Невозможно удалить статус, потому что он используется'
        )

    def test_delete_user_if_related(self):
        response = self.client.post(reverse('delete_user', kwargs={'pk': 1}))

        self.assertRedirects(response, reverse('users'))
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Невозможно удалить пользователя, потому что он используется'
        )

    def test_delete_label_if_related(self):
        response = self.client.post(reverse('delete_label', kwargs={'pk': 1}))

        self.assertRedirects(response, reverse('labels'))
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Невозможно удалить метку, потому что она используется'
        )


class TasksFilterTest(SetUpTestCase):
    def test_filter_tasks_by_status(self):
        response = self.client.get(reverse('tasks'), {'status': 1})
        tasks = response.context['tasks']
        self.assertEqual(tasks.count(), 3)

    def test_filter_tasks_by_label(self):
        response = self.client.get(reverse('tasks'), {'label': 1})
        tasks = response.context['tasks']
        self.assertEqual(tasks.count(), 1)

    def test_filter_tasks_by_executor(self):
        response = self.client.get(reverse('tasks'), {'executor': 2})
        tasks = response.context['tasks']
        self.assertEqual(tasks.count(), 2)

    def test_filter_tasks_by_fields(self):
        response = self.client.get(reverse('tasks'),
                                   {'status': 1, 'executor': 1, 'label': 1})
        tasks = response.context['tasks']
        self.assertEqual(tasks.count(), 1)

        response = self.client.get(reverse('tasks'),
                                   {'status': 1, 'executor': 2, 'label': 2})
        tasks = response.context['tasks']
        self.assertEqual(tasks.count(), 2)
