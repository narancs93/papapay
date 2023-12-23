from django.contrib import auth
from django.test import Client, TestCase
from django.urls import reverse

from papapay.user.models import User
from papapay.user.serializers import LoginSerializer


class TestLogin(TestCase):

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
        self.login_url = reverse('papapay.user:login')
        self.empty_email_error = 'Email address is required. Please enter a valid email.'
        self.empty_password_error = 'Password is required.'
        self.invalid_user_or_pw_error = 'Invalid email or password.'

    def test_login_GET(self):
        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/login.html')
        self.assertTrue('serializer' in response.context)
        self.assertIsInstance(response.context['serializer'], LoginSerializer)

    def test_login_GET_redirects_to_home_if_authenticated(self):
        self.client.login(email=self.email, password=self.password)
        user = auth.get_user(self.client)
        response = self.client.get(self.login_url)

        self.assertTrue(user.is_authenticated)
        self.assertRedirects(response, expected_url=reverse('papapay.home:home-url'),
                             status_code=302, target_status_code=200)
        self.client.logout()

    def test_login_POST_no_data(self):
        response = self.client.post(self.login_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/login.html')
        self.assertTrue('serializer' in response.context)
        self.assertIsInstance(response.context['serializer'], LoginSerializer)

        email_errors = response.context['serializer'].errors.get('email', [])
        password_errors = response.context['serializer'].errors.get('password', [])

        self.assertTrue(self.empty_email_error in email_errors)
        self.assertTrue(self.empty_password_error in password_errors)

    def test_login_POST_wrong_email(self):
        response = self.client.post(self.login_url, data={
            'email': 'wrong.email@example.com',
            'password': self.password,
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/login.html')
        self.assertTrue('serializer' in response.context)
        self.assertIsInstance(response.context['serializer'], LoginSerializer)

        email_errors = response.context['serializer'].errors.get('email', [])
        password_errors = response.context['serializer'].errors.get('password', [])

        self.assertEqual(email_errors, [])
        self.assertTrue(self.invalid_user_or_pw_error in password_errors)

    def test_login_POST_wrong_password(self):
        response = self.client.post(self.login_url, data={
            'email': self.email,
            'password': 'wrongPassword',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/login.html')
        self.assertTrue('serializer' in response.context)
        self.assertIsInstance(response.context['serializer'], LoginSerializer)

        email_errors = response.context['serializer'].errors.get('email', [])
        password_errors = response.context['serializer'].errors.get('password', [])

        self.assertEqual(email_errors, [])
        self.assertTrue(self.invalid_user_or_pw_error in password_errors)

    def test_login_POST_successful_authentication(self):
        response = self.client.post(self.login_url, data={
            'email': self.email,
            'password': self.password
        })

        self.assertRedirects(response, expected_url=reverse('papapay.home:home-url'),
                             status_code=302, target_status_code=200)
