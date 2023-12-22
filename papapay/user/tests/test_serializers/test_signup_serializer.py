from django.contrib.auth import get_user_model
from django.test import TestCase

from papapay.user.serializers import SignupSerializer

User = get_user_model()


class SignupSerializerTest(TestCase):

    def test_serialize_user(self):
        user_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test.user@example.com',
            'password': 'password123',
        }
        user = User.objects.create(**user_data)
        serializer = SignupSerializer(user)
        expected_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test.user@example.com',
        }
        self.assertEqual(serializer.data, expected_data)

    def test_deserialize_user(self):
        signup_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test.user@example.com',
            'password': 'SuperSecretPassword123!',
            'password2': 'SuperSecretPassword123!'
        }
        serializer = SignupSerializer(data=signup_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.first_name, signup_data['first_name'])
        self.assertEqual(user.last_name, signup_data['last_name'])
        self.assertEqual(user.email, signup_data['email'])
