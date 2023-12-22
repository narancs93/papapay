from django.test import Client, TestCase
from django.urls import reverse

from papapay.user.models import User


class LogoutTest(TestCase):

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

    def test_logout(self):
        response = self.client.get(reverse('papapay.home:home-url'))
        self.assertEquals(response.status_code, 200)
        self.assertIn('Logout', response.content.decode('utf-8'))

        logout_response = self.client.get(reverse('papapay.user:logout'))

        self.assertRedirects(logout_response, reverse('papapay.home:home-url'),
                             status_code=302, target_status_code=200)

        response = self.client.get(reverse('papapay.home:home-url'))
        self.assertEquals(response.status_code, 200)
        self.assertIn('Login', response.content.decode('utf-8'))
