from django.contrib.auth import get_user_model
from django.test import TestCase

from papapay.user.models import UserManager

User = get_user_model()


class UserManagerTest(TestCase):

    def setUp(self):
        self.user_manager = UserManager()
        self.user_manager.model = User

    def test_create_user_raises_value_error(self):
        with self.assertRaisesMessage(ValueError, 'User must have email address, first name and last name.'):
            self.user_manager._create_user(email='', first_name='', last_name='', password='password123')

    def test_create_superuser_sets_defaults_for_is_staff_and_is_superuser(self):
        created_user = self.user_manager.create_superuser(
            email='admin@admin.com', first_name='Admin', last_name='Admin', password='admin')

        self.assertTrue(created_user.is_staff)
        self.assertTrue(created_user.is_superuser)

    def test_create_superuser_raises_error_if_is_staff_false(self):
        with self.assertRaisesMessage(ValueError, 'Superuser must have is_staff=True.'):
            self.user_manager.create_superuser(
                email='admin@admin.com', first_name='Admin', last_name='Admin', password='admin', is_staff=False)

    def test_create_superuser_raises_error_if_is_superuser_false(self):
        with self.assertRaisesMessage(ValueError, 'Superuser must have is_superuser=True.'):
            self.user_manager.create_superuser(
                email='admin@admin.com', first_name='Admin', last_name='Admin', password='admin', is_superuser=False)
