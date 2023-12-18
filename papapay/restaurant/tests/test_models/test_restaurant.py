from papapay.restaurant.models import Restaurant
from .base_setup_test import BaseSetupTest


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
