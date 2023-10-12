from .models import Status
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from task_manager.users.models import User


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


class StatusCreateTestCase(SetUpTestCase):

    def test_create_status(self):

        response = self.client.post(reverse('create_status'), {'name': 'New'})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Статус успешно создан')

    def test_create_status_if_not_logged_in(self):

        self.client.logout()

        response = self.client.get(reverse('create_status'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]),
                         'Вы не авторизованы! Пожалуйста, выполните вход.'
                         )

    def test_statuses_access_if_not_logged_in(self):

        self.client.logout()
        response = self.client.get(reverse('statuses'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]),
                         'Вы не авторизованы! Пожалуйста, выполните вход.'
                         )


class StatusUpdateTestCase(SetUpTestCase):
    def test_update_status(self):

        response = self.client.post(reverse('update_status', kwargs={'pk': 1}),
                                    {'name': 'In work'})

        self.assertRedirects(response, reverse('statuses'))
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Статус успешно изменен')

    def test_update_status_if_not_logged_in(self):

        self.client.logout()
        response = self.client.get(reverse('update_status', kwargs={'pk': 1}))

        self.assertRedirects(response, reverse('login'))
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]),
                         'Вы не авторизованы! Пожалуйста, выполните вход.')


class StatusDeleteTestCase(SetUpTestCase):
    def test_delete_status(self):

        response = self.client.post(reverse('delete_status', kwargs={'pk': 1}))

        self.assertRedirects(response, reverse('statuses'))
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Статус успешно удален')

    def test_delete_status_if_not_logged_in(self):

        self.client.logout()
        response = self.client.get(reverse('delete_status', kwargs={'pk': 1}))

        self.assertRedirects(response, reverse('login'))
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]),
                         'Вы не авторизованы! Пожалуйста, выполните вход.')
