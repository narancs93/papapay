from django.core.exceptions import ValidationError

from papapay.postal_address.models import Country

from .base_setup_test import BaseSetupTest


class CountryTest(BaseSetupTest):
    def test_create_and_save_model(self):
        country = Country(name='Test Country', alpha3_code='XYZ')
        country.save()

        saved_country = Country.objects.get(id=country.id)
        self.assertEqual(saved_country.name, 'Test Country')
        self.assertEqual(saved_country.alpha3_code, 'XYZ')

    def test_unique_name_is_enforced(self):
        with self.assertRaises(ValidationError):
            Country.objects.create(name='Example Country', alpha3_code='AB')

    def test_name_mandatory_is_enforced(self):
        with self.assertRaises(ValidationError):
            Country.objects.create(alpha3_code='X')

    def test_alpha3_code_blank_by_default(self):
        created_country = Country.objects.create(name='Country without Alpha 3 Code')

        self.assertEqual(created_country.alpha3_code, '')

    def test_international_call_prefix_blank_by_default(self):
        created_country = Country.objects.create(name='Country without Call Prefix')

        self.assertEqual(created_country.international_call_prefix, '')

    def test_str(self):
        expected = f'Example Country (id={self.country.id})'
        actual = str(self.country)

        self.assertEqual(expected, actual)
