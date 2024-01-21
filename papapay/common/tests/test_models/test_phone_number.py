from django.db.utils import IntegrityError

from papapay.common.models import PhoneNumber
from ..base_setup_test import BaseSetupTest


class PhoneNumberTest(BaseSetupTest):
    def test_create_and_save_model(self):
        phone_number = PhoneNumber(
            name='Landline Phone',
            country=self.country,
            phone_number='6059713696',
            owner=self.restaurant)
        phone_number.save()

        saved_phone_number = PhoneNumber.objects.get(id=phone_number.id)
        self.assertEqual(saved_phone_number.name, 'Landline Phone')

    def test_unique_country_and_phone_number_together_is_enforced(self):
        with self.assertRaises(IntegrityError):
            PhoneNumber.objects.create(country=self.country, phone_number='6059713695', owner=self.restaurant)

    def test_str(self):
        expected = f'+1 6059713695 (id={self.phone_number.id})'
        actual = str(self.phone_number)

        self.assertEqual(expected, actual)

    def test_str_without_prefix(self):
        expected = f'6059713600 (id={self.phone_number_without_prefix.id})'
        actual = str(self.phone_number_without_prefix)

        self.assertEqual(expected, actual)

    def test_repr(self):
        expected = 'Example Phone Number (+1 6059713695)'
        actual = repr(self.phone_number)

        self.assertEqual(expected, actual)
