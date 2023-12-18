from django.test import TestCase

from papapay.postal_address.models import (City, Country, District,
                                           PostalAddress, State, Street)


class BaseSetupTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name='Example Country', initials='AB')
        self.state = State.objects.create(name='Example State', initials='AB', area_code='A-001', country=self.country)
        self.city = City.objects.create(name='Example City', state=self.state)
        self.district = District.objects.create(name='Example District', city=self.city)
        self.street = Street.objects.create(name='Example Street', zip_code='ZIP123', district=self.district)
        self.postal_address = PostalAddress.objects.create(street=self.street, house_number='1', floor_number='2',
                                                           door_number='3', note='Example Note')
