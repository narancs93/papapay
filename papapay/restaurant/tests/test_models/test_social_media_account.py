from papapay.restaurant.models import SocialMediaAccount
from .base_setup_test import BaseSetupTest


class SocialMediaAccountTest(BaseSetupTest):
    def test_create_and_save_model(self):
        social_media_account = SocialMediaAccount(
            restaurant=self.restaurant,
            platform='facebook',
            username='test_username'
        )
        social_media_account.save()
        self.assertEqual(social_media_account.restaurant, self.restaurant)
        self.assertEqual(social_media_account.platform, 'facebook')
        self.assertEqual(social_media_account.username, 'test_username')
