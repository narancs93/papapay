from django.core.exceptions import ValidationError

from papapay.postal_address.models import PostalAddress

from papapay.common.tests.base_setup_test import BaseSetupTest


class PostalAddressTest(BaseSetupTest):
    def test_create_and_save_model(self):
        postal_address = PostalAddress(street=self.street, house_number='42', floor_number='5',
                                       door_number='3', note='Test Note')
        postal_address.save()

        saved_postal_address = PostalAddress.objects.get(id=postal_address.id)
        self.assertEqual(saved_postal_address.street, self.street)
        self.assertEqual(saved_postal_address.house_number, '42')
        self.assertEqual(saved_postal_address.floor_number, '5')
        self.assertEqual(saved_postal_address.door_number, '3')
        self.assertEqual(saved_postal_address.note, 'Test Note')

    def test_street_mandatory_is_enforced(self):
        with self.assertRaises(ValidationError):
            PostalAddress.objects.create(house_number='123')

    def test_house_number_mandatory_is_enforced(self):
        with self.assertRaises(ValidationError):
            PostalAddress.objects.create(street=self.street)

    def test_floor_number_blank_by_default(self):
        postal_address = PostalAddress(street=self.street, house_number='50', door_number='1', note='Test Note')

        self.assertEqual(postal_address.floor_number, '')

    def test_door_number_blank_by_default(self):
        postal_address = PostalAddress(street=self.street, house_number='51', floor_number='2', note='Test Note')

        self.assertEqual(postal_address.door_number, '')

    def test_note_blank_by_default(self):
        postal_address = PostalAddress(street=self.street, house_number='52', floor_number='3', door_number='2')

        self.assertEqual(postal_address.note, '')

    def test_str(self):
        expected = f'31st Ave, 1234, 2/3 (id={self.postal_address.id})'
        actual = str(self.postal_address)

        self.assertEqual(expected, actual)
