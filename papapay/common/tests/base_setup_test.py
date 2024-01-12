from django.contrib.auth import get_user_model
from django.test import TestCase

from papapay.common.models import PhoneNumber
from papapay.postal_address.models import (City, Country, District,
                                           PostalAddress, State, Street)
from papapay.postal_address.utils import create_postal_address
from papapay.restaurant.models import Restaurant, SocialMediaAccount

User = get_user_model()


class BaseSetupTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            first_name='Example',
            last_name='User',
            email='example.user@example.com')

        self.country = Country.objects.create(
            name='United States of America', alpha2_code='US', alpha3_code='USA', international_call_prefix='+1')

        self.user_phone_number = PhoneNumber.objects.create(
            name='Example Phone Number for Example User',
            country=self.country,
            phone_number='1234556787',
            owner=self.user)

        self.country_without_prefix = Country.objects.create(
            name='Example Country', alpha3_code='EXA')

        self.state = State.objects.create(
            name='Example State',
            abbreviation='AB',
            area_code='A-001',
            country=self.country)

        self.city = City.objects.create(
            name='Example City',
            state=self.state)

        self.district = District.objects.create(
            name='Example District',
            city=self.city)

        self.street = Street.objects.create(
            name='Example Street',
            zip_code='ZIP123',
            district=self.district)

        self.postal_address = PostalAddress.objects.create(
            street=self.street,
            house_number='1',
            floor_number='2',
            door_number='3',
            note='Example Note')

        self.postal_address = create_postal_address(
            country_name='United States of America',
            state_name='California',
            city_name='San Fransisco',
            district_name='Sunset District',
            street_zip_code='94116',
            street_name='31st Ave',
            house_number='1234',
            floor_number='2',
            door_number='3',)

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

        self.phone_number_without_prefix = PhoneNumber.objects.create(
            name='Example Phone Number without Prefix',
            country=self.country_without_prefix,
            phone_number='6059713600',
            owner=self.restaurant)

        self.social_media_account = SocialMediaAccount.objects.create(
                restaurant=self.restaurant,
                platform='facebook',
                username='example_username'
            )
