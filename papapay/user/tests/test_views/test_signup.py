from django.contrib import auth
from django.test import Client, TestCase
from django.urls import reverse

from papapay.user.models import User
from papapay.user.serializers import SignupSerializer


class SignupTest(TestCase):

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
        self.signup_url = reverse('papapay.user:signup')
        self.empty_first_name_error = 'First name is required.'
        self.empty_last_name_error = 'Last name is required.'
        self.empty_email_error = 'Email address is required. Please enter a valid email.'
        self.empty_password_error = 'Password is required.'
        self.empty_confirm_password_error = 'Confirm password is required.'
        self.used_email_error = 'This email address is already in use.'
        self.password_too_common_error = 'This password is too common.'
        self.password_mismatch_error = 'Password fields didn\'t match.'

    def test_signup_GET(self):
        response = self.client.get(self.signup_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/signup.html')
        self.assertTrue('serializer' in response.context)
        self.assertIsInstance(response.context['serializer'], SignupSerializer)

    def test_login_GET_redirects_to_home_if_authenticated(self):
        self.client.login(email=self.email, password=self.password)
        user = auth.get_user(self.client)
        response = self.client.get(self.signup_url)

        self.assertTrue(user.is_authenticated)
        self.assertRedirects(response, expected_url=reverse('papapay.home:home-url'),
                             status_code=302, target_status_code=200)
        self.client.logout()

    def test_signup_POST_no_data(self):
        response = self.client.post(self.signup_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/signup.html')
        self.assertTrue('serializer' in response.context)
        self.assertIsInstance(response.context['serializer'], SignupSerializer)

        serializer_errors = response.context['serializer'].errors

        first_name_errors = serializer_errors.get('first_name', [])
        last_name_errors = serializer_errors.get('last_name', [])
        email_errors = serializer_errors.get('email', [])
        password_errors = serializer_errors.get('password', [])
        confirm_password_errors = serializer_errors.get('password2', [])

        self.assertIn(self.empty_first_name_error, first_name_errors)
        self.assertIn(self.empty_last_name_error, last_name_errors)
        self.assertIn(self.empty_email_error, email_errors)
        self.assertIn(self.empty_password_error, password_errors)
        self.assertIn(self.empty_confirm_password_error, confirm_password_errors)

    def test_signup_POST_email_in_use(self):
        response = self.client.post(self.signup_url, data={
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'example.user@example.com',
            'password': 'SuperSecretPassword!123',
            'password2': 'SuperSecretPassword!123',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/signup.html')
        self.assertTrue('serializer' in response.context)
        self.assertIsInstance(response.context['serializer'], SignupSerializer)

        serializer_errors = response.context['serializer'].errors
        email_errors = serializer_errors.get('email')

        self.assertIn(self.used_email_error, email_errors)

    def test_signup_POST_password_too_simple(self):
        response = self.client.post(self.signup_url, data={
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'simple.password@example.com',
            'password': 'password',
            'password2': 'password',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/signup.html')
        self.assertTrue('serializer' in response.context)
        self.assertIsInstance(response.context['serializer'], SignupSerializer)

        serializer_errors = response.context['serializer'].errors
        password_errors = serializer_errors.get('password')

        self.assertIn(self.password_too_common_error, password_errors)

    def test_signup_POST_passwords_not_match(self):
        response = self.client.post(self.signup_url, data={
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'password.mismatch@example.com',
            'password': 'SuperSecretPassword!123',
            'password2': 'SuperSecretPassword!1234',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/signup.html')
        self.assertTrue('serializer' in response.context)
        self.assertIsInstance(response.context['serializer'], SignupSerializer)

        serializer_errors = response.context['serializer'].errors
        password_errors = serializer_errors.get('password')

        self.assertIn(self.password_mismatch_error, password_errors)

    def test_signup_POST_successful(self):
        response = self.client.post(self.signup_url, data={
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test.user@example.com',
            'password': 'SuperSecretPassword!123',
            'password2': 'SuperSecretPassword!123',
        })

        self.assertRedirects(response, expected_url=reverse('papapay.user:login'),
                             status_code=302, target_status_code=200)
