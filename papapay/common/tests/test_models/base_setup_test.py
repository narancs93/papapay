from django.test import TestCase

from papapay.common.models import PhoneNumber
from papapay.postal_address.models import Country
from papapay.restaurant.models import Restaurant
from papapay.postal_address.utils import create_postal_address


class BaseSetupTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(
            name='United States of America', alpha3_code='USA', international_call_prefix='1')

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
            email_address='example.restaurant@example.com',
            postal_address=self.postal_address)

        self.phone_number = PhoneNumber.objects.create(
            name='Example Phone Number',
            country=self.country,
            phone_number='6059713695',
            owner=self.restaurant)
