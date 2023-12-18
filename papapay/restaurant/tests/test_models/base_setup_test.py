from django.test import TestCase

from papapay.postal_address.utils import create_postal_address
from papapay.restaurant.models import Restaurant


class BaseSetupTest(TestCase):
    def setUp(self):
        self.postal_address = create_postal_address(
            country_name='United States of America',
            state_name='California',
            city_name='San Fransisco',
            district_name='Sunset District',
            street_zip_code='94116',
            street_name='31st Ave',
            house_number='1234')

        self.restaurant = Restaurant.objects.create(
            name='Example Restaurant',
            description='Example Restaurant Description',
            introduction='Example Restaurant Introduction',
            email_address='example@restaurant.com',
            postal_address=self.postal_address
        )
