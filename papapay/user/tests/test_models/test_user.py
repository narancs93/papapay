from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase

User = get_user_model()


class UserTest(TestCase):
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

    def test_create_and_save_model(self):
        user = User(
            first_name='Test',
            last_name='User',
            email='test.user@example.com',
            password='password123'
        )
        user.save()

        saved_user = User.objects.get(id=user.id)
        self.assertEqual(saved_user.first_name, 'Test')
        self.assertEqual(saved_user.last_name, 'User')
        self.assertEqual(saved_user.email, 'test.user@example.com')

    def test_user_can_authenticate(self):
        authenticated = self.client.login(email=self.email, password=self.password)
        self.assertTrue(authenticated)

    def test_unique_email_is_enforced(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email=self.email,
                first_name='Test',
                last_name='User',
                password='password123'
            )

    def test_str(self):
        expected = f'example.user@example.com (id={self.user.id})'
        actual = str(self.user)

        self.assertEqual(expected, actual)
