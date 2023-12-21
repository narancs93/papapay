from django.contrib.auth import get_user_model
from django.test import TestCase

from papapay.user.serializers import LoginSerializer

User = get_user_model()


class LoginSerializerTest(TestCase):

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

    def test_serialize_user(self):
        user_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test.user@example.com',
            'password': 'password123',
        }
        user = User.objects.create(**user_data)
        serializer = LoginSerializer(user)
        expected_data = {
            'email': 'test.user@example.com',
        }
        self.assertEqual(serializer.data, expected_data)

    def test_deserialize_user(self):
        registration_data = {
            'email': self.email,
            'password': self.password,
        }
        serializer = LoginSerializer(data=registration_data)
        is_valid = serializer.is_valid()
        authenticated_user = serializer.get_authenticated_user()

        self.assertTrue(is_valid)
        self.assertEqual(authenticated_user, self.user)
