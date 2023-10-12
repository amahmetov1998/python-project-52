from .models import Label
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

        self.label = Label.objects.create(name='Label')
        self.label.save()


class LabelCreateTestCase(SetUpTestCase):

    def test_create_label(self):

        response = self.client.post(reverse('create_label'), {'name': 'Text'})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Метка успешно создана')

    def test_create_label_if_not_logged_in(self):

        self.client.logout()

        response = self.client.get(reverse('create_label'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]),
                         'Вы не авторизованы! Пожалуйста, выполните вход.')

    def test_labels_access_if_not_logged_in(self):

        self.client.logout()
        response = self.client.get(reverse('labels'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]),
                         'Вы не авторизованы! Пожалуйста, выполните вход.')


class LabelUpdateTestCase(SetUpTestCase):
    def test_update_label(self):

        response = self.client.post(reverse('update_label', kwargs={'pk': 1}),
                                    {'name': 'Labels'})

        self.assertRedirects(response, reverse('labels'))
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Метка успешно изменена')

    def test_update_label_if_not_logged_in(self):

        self.client.logout()
        response = self.client.get(reverse('update_label', kwargs={'pk': 1}))

        self.assertRedirects(response, reverse('login'))
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]),
                         'Вы не авторизованы! Пожалуйста, выполните вход.')


class LabelDeleteTestCase(SetUpTestCase):
    def test_delete_label(self):

        response = self.client.post(reverse('delete_label', kwargs={'pk': 1}))

        self.assertRedirects(response, reverse('labels'))
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Метка успешно удалена')

    def test_delete_label_if_not_logged_in(self):

        self.client.logout()
        response = self.client.get(reverse('delete_label', kwargs={'pk': 1}))

        self.assertRedirects(response, reverse('login'))
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]),
                         'Вы не авторизованы! Пожалуйста, выполните вход.')
