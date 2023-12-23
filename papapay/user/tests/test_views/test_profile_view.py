from django.test import Client, TestCase
from django.urls import reverse

from papapay.user.models import User
from papapay.user.serializers import PasswordUpdateSerializer, UserProfileSerializer


class ProfileViewTest(TestCase):

    def setUp(self):
        self.email = 'example.user@example.com'
        self.first_name = 'Example'
        self.last_name = 'User'
        self.password = 'password123'
        self.user = User.objects.create_user(
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            password=self.password)

        self.client = Client()
        self.client.login(email=self.email, password=self.password)
        self.profile_url = reverse('papapay.user:profile')
        self.login_url = reverse('papapay.user:login')

        self.empty_first_name_error = 'First name is required.'
        self.empty_last_name_error = 'Last name is required.'
        self.empty_email_error = 'Email address is required. Please enter a valid email.'
        self.empty_password_error = 'Password is required.'
        self.empty_confirm_password_error = 'Confirm password is required.'
        self.used_email_error = 'This email address is already in use.'
        self.password_too_common_error = 'This password is too common.'
        self.password_mismatch_error = 'Password fields didn\'t match.'

    def assert_common_profile_page_assertions(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/profile.html')
        self.assertIn('profile_serializer', response.context)
        self.assertIsInstance(response.context['profile_serializer'], UserProfileSerializer)
        self.assertIn('password_update_serializer', response.context)
        self.assertIsInstance(response.context['password_update_serializer'], PasswordUpdateSerializer)

    def test_profile_GET(self):
        response = self.client.get(self.profile_url)

        self.assert_common_profile_page_assertions(response)

    def test_profile_GET_requires_auth(self):
        response = Client().get(self.profile_url)

        self.assertRedirects(response, expected_url=f"{self.login_url}?next={self.profile_url}",
                             status_code=302, target_status_code=200)

    def test_POST_requires_auth(self):
        response = Client().post(self.profile_url, data={})

        self.assertRedirects(response, expected_url=f"{self.login_url}?next={self.profile_url}",
                             status_code=302, target_status_code=200)

    def test_profile_POST_no_data_does_not_change_user(self):
        response = self.client.post(self.profile_url, data={})

        self.assert_common_profile_page_assertions(response)

        user = User.objects.get(pk=self.user.id)
        self.assertEqual(user.email, self.user.email)
        self.assertEqual(user.first_name, self.user.first_name)
        self.assertEqual(user.last_name, self.user.last_name)
        self.assertTrue(user.check_password(self.password))

    def test_profile_POST_update_profile(self):
        post_data = {
            '_update_type': 'profile',
            'email': 'updated.email@example.com',
            'first_name': 'Updated First Name',
            'last_name': 'Updated Last Name'
        }
        response = self.client.post(self.profile_url, data=post_data)
        updated_user = User.objects.get(pk=self.user.id)

        self.assert_common_profile_page_assertions(response)

        self.assertEqual(updated_user.email, post_data['email'])
        self.assertEqual(updated_user.first_name, post_data['first_name'])
        self.assertEqual(updated_user.last_name, post_data['last_name'])

    def test_profile_POST_update_profile_no_data_displays_errors(self):
        response = self.client.post(self.profile_url, data={
            '_update_type': 'profile',
            'email': '',
            'first_name': '',
            'last_name': ''
        })

        self.assert_common_profile_page_assertions(response)

        validation_errors = response.context['profile_serializer'].errors
        self.assertIn('Email address is required. Please enter a valid email.', validation_errors['email'])
        self.assertIn('First name is required.', validation_errors['first_name'])
        self.assertIn('Last name is required.', validation_errors['last_name'])

    def test_profile_POST_update_password(self):
        new_password = 'SuperSecretPassword123!'
        post_data = {
            '_update_type': 'password',
            'password': self.password,
            'new_password': new_password,
            'new_password2': new_password,
        }
        response = self.client.post(self.profile_url, data=post_data)
        updated_user = User.objects.get(pk=self.user.id)

        self.assert_common_profile_page_assertions(response)

        self.assertTrue(updated_user.check_password(new_password))

    def test_profile_POST_update_password_no_data(self):
        response = self.client.post(self.profile_url, data={
            '_update_type': 'password',
            'password': '',
            'new_password': '',
            'new_password2': '',
        })
        validation_errors = response.context['password_update_serializer'].errors

        self.assert_common_profile_page_assertions(response)

        self.assertIn('Current password does not match.', validation_errors['password'])

    def test_profile_POST_update_password_new_passwords_mismatch(self):
        response = self.client.post(self.profile_url, data={
            '_update_type': 'password',
            'password': self.password,
            'new_password': 'SuperSecretPassword123',
            'new_password2': 'SuperSecretPassword1234',
        })
        validation_errors = response.context['password_update_serializer'].errors

        self.assert_common_profile_page_assertions(response)

        self.assertIn('Password fields didn\'t match.', validation_errors['new_password'])
