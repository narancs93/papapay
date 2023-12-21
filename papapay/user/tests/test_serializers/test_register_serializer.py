from django.contrib.auth import get_user_model
from django.test import TestCase

from papapay.user.serializers import RegisterSerializer

User = get_user_model()


class RegisterSerializerTest(TestCase):

    def test_serialize_user(self):
        user_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test.user@example.com',
            'password': 'password123',
        }
        user = User.objects.create(**user_data)
        serializer = RegisterSerializer(user)
        expected_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test.user@example.com',
        }
        self.assertEqual(serializer.data, expected_data)

    def test_deserialize_user(self):
        registration_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test.user@example.com',
            'password': 'SuperSecretPassword123!',
            'password2': 'SuperSecretPassword123!'
        }
        serializer = RegisterSerializer(data=registration_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.first_name, registration_data['first_name'])
        self.assertEqual(user.last_name, registration_data['last_name'])
        self.assertEqual(user.email, registration_data['email'])
