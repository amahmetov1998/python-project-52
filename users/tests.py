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


class UserCreateTestCase(SetUpTestCase):
    def test_user_creation(self):
        user = self.user

        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(str(user), 'john_lennon')

    def test_user_registration_success(self):
        response = self.client.post(
            reverse('register'),
            {'first_name': 'Katy', 'last_name': 'Perry',
             'username': 'katy_perry', 'password1': 'kBPfn673ls',
             'password2': 'kBPfn673ls'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Пользователь успешно зарегистрирован')


class UserUpdateTestCase(SetUpTestCase):
    def test_update_user(self):
        response = self.client.post(
            reverse('update', kwargs={'pk': 1}),
            {'first_name': 'John', 'last_name': 'Lennon',
             'username': 'johny', 'password1': 'gtJej43j95',
             'password2': 'gtJej43j95'}
        )

        self.assertRedirects(response, reverse('users'))
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Пользователь успешно изменен')

    def test_update_user_if_no_permission(self):
        response = self.client.post(
            reverse('update', kwargs={'pk': 2}),
            {'first_name': 'Kate', 'last_name': 'Perry',
             'username': 'kate_perry', 'password1': 'kBPfn673ls',
             'password2': 'kBPfn673ls'}
        )

        self.assertRedirects(response, reverse('users'))
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'У вас нет прав для изменения другого пользователя.')

    def test_update_user_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('update', kwargs={'pk': 1}))
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Вы не авторизованы! Пожалуйста, выполните вход.')


class UserDeleteTestCase(SetUpTestCase):
    def test_delete_user(self):
        response = self.client.post(reverse('delete', kwargs={'pk': 1}))

        self.assertRedirects(response, reverse('users'))
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Пользователь успешно удален')

    def test_delete_user_if_no_permission(self):
        response = self.client.post(reverse('delete', kwargs={'pk': 2}))

        self.assertRedirects(response, reverse('users'))
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'У вас нет прав для изменения другого пользователя.')

    def test_delete_user_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('delete', kwargs={'pk': 1}))
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Вы не авторизованы! Пожалуйста, выполните вход.')
