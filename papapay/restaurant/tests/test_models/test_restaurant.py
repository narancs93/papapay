from django.core.exceptions import ValidationError

from papapay.restaurant.models import Restaurant

from papapay.common.tests.base_setup_test import BaseSetupTest


class RestaurantTest(BaseSetupTest):
    def test_create_and_save_model(self):
        restaurant = Restaurant(
            name='Test Restaurant',
            description='Test Restaurant Description',
            introduction='Test Restaurant Introduction',
            email_address='test@restaurant.com',
            postal_address=self.postal_address
        )
        restaurant.save()

        self.assertEqual(restaurant.name, 'Test Restaurant')
        self.assertEqual(restaurant.description, 'Test Restaurant Description')
        self.assertEqual(restaurant.introduction, 'Test Restaurant Introduction')
        self.assertEqual(restaurant.email_address, 'test@restaurant.com')
        self.assertEqual(restaurant.postal_address, self.postal_address)

    def test_unique_name_is_enforced(self):
        with self.assertRaises(ValidationError):
            Restaurant.objects.create(
                name='Example Restaurant',
                description='Example Restaurant Description',
                introduction='Example Restaurant Introduction',
                email_address='example@restaurant.com',
                postal_address=self.postal_address,
            )

    def test_mandatory_description_is_enforced(self):
        with self.assertRaises(ValidationError):
            Restaurant.objects.create(
                name='Example Restaurant without Description',
                introduction='Example Restaurant Introduction',
                email_address='example@restaurant.com',
                postal_address=self.postal_address,
            )

    def test_mandatory_introduction_is_enforced(self):
        with self.assertRaises(ValidationError):
            Restaurant.objects.create(
                name='Example Restaurant without Introduction',
                description='Example Restaurant Description',
                email_address='example@restaurant.com',
                postal_address=self.postal_address,
            )

    def test_mandatory_email_address_is_enforced(self):
        with self.assertRaises(ValidationError):
            Restaurant.objects.create(
                name='Example Restaurant without Email Address',
                description='Example Restaurant Description',
                introduction='Example Restaurant Introduction',
                postal_address=self.postal_address,
            )

    def test_str(self):
        expected = f"Example Restaurant (id={self.restaurant.id})"
        actual = str(self.restaurant)

        self.assertEqual(expected, actual)
