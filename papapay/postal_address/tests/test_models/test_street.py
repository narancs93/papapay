from django.core.exceptions import ValidationError

from papapay.common.tests.base_setup_test import BaseSetupTest
from papapay.postal_address.models import Street


class StreetTest(BaseSetupTest):
    def test_create_and_save_model(self):
        street = Street(name='Test Street', zip_code='ABC123', district=self.district)
        street.save()

        saved_street = Street.objects.get(id=street.id)
        self.assertEqual(saved_street.name, 'Test Street')
        self.assertEqual(saved_street.district, self.district)

    def test_unique_name_and_district_together_is_enforced(self):
        with self.assertRaises(ValidationError):
            Street.objects.create(name='Example Street', zip_code='0', district=self.district)

    def test_str(self):
        expected = f'Example Street (Example District) (id={self.street.id})'
        actual = str(self.street)

        self.assertEqual(expected, actual)
