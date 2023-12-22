from django.test import SimpleTestCase
from django.urls import resolve, reverse

from papapay.user.views import LoginView, LogoutView, SignupView


class TestUrls(SimpleTestCase):

    def test_login_url_resolves(self):
        url = reverse('papapay.user:login')
        self.assertEqual(resolve(url).func.view_class, LoginView)

    def test_signup_url_resolves(self):
        url = reverse('papapay.user:signup')
        self.assertEqual(resolve(url).func.view_class, SignupView)

    def test_logout_url_resolves(self):
        url = reverse('papapay.user:logout')
        self.assertEqual(resolve(url).func.view_class, LogoutView)
