from django.test import Client, TestCase
from django.urls import reverse

from ....common.models import Country, PhoneNumber
from ....user.models import User


class RemovePhoneNumberFromUserTest(TestCase):

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

        country = Country.objects.create(
            name='United States of America',
            alpha2_code='US',
            alpha3_code='USA',
            international_call_prefix='+1')

        self.phone_number = PhoneNumber.objects.create(
            name='Example Phone Number for Example User',
            country=country,
            phone_number='1234556787',
            owner=self.user)

        self.client = Client()
        self.client.login(email=self.email, password=self.password)
        self.remove_phone_number_url = reverse('papapay.user:remove-phone-number-from-profile-api')

        self.empty_first_name_error = 'First name is required.'
        self.empty_last_name_error = 'Last name is required.'
        self.empty_email_error = 'Email address is required. Please enter a valid email.'
        self.empty_password_error = 'Password is required.'
        self.empty_confirm_password_error = 'Confirm password is required.'
        self.used_email_error = 'This email address is already in use.'
        self.password_too_common_error = 'This password is too common.'
        self.password_mismatch_error = 'Password fields didn\'t match.'

    def test_delete_phone_number_POST(self):
        post_data = {
            'phone_number_id': self.phone_number.id}
        response = self.client.post(self.remove_phone_number_url, data=post_data)
        self.assertEquals(response.status_code, 200)

        with self.assertRaises(PhoneNumber.DoesNotExist):
            PhoneNumber.objects.get(id=self.phone_number.id)

    def test_delete_phone_number_POST_requires_auth(self):
        post_data = {
            'phone_number_id': self.phone_number.id}
        response = Client().post(self.remove_phone_number_url, data=post_data)
        self.assertEquals(response.status_code, 400)

    def test_delete_another_users_phone_number_POST(self):
        other_user = User.objects.create_user(
            email='other_user@example.com',
            first_name='Other',
            last_name='Test User',
            password='password123')
        self.client.login(email=other_user.email, password=other_user.password)
        post_data = {
            'phone_number_id': self.phone_number.id}
        response = Client().post(self.remove_phone_number_url, data=post_data)
        self.assertEquals(response.status_code, 400)
