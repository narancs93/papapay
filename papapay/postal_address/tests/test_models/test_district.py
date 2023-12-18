from django.core.exceptions import ValidationError

from papapay.postal_address.models import District

from .base_setup_test import BaseSetupTest


class DistrictTest(BaseSetupTest):
    def test_create_and_save_model(self):
        district = District(name='Test District', city=self.city)
        district.save()

        saved_district = District.objects.get(id=district.id)
        self.assertEqual(saved_district.name, 'Test District')
        self.assertEqual(saved_district.city, self.city)

    def test_unique_name_and_city_together_is_enforced(self):
        with self.assertRaises(ValidationError):
            District.objects.create(name='Example District', city=self.city)

    def test_name_mandatory_is_enforced(self):
        with self.assertRaises(ValidationError):
            District.objects.create(city=self.city)

    def test_city_mandatory_is_enforced(self):
        with self.assertRaises(ValidationError):
            District.objects.create(name='District without City')

    def test_str(self):
        expected = f'Example District (Example City) (id={self.district.id})'
        actual = str(self.district)

        self.assertEqual(expected, actual)
