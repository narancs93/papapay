from django.contrib.auth import get_user_model

from ..base_setup_test import BaseSetupTest
from ...serializers import PhoneNumberSerializer

User = get_user_model()


class PhoneNumberSerializerTest(BaseSetupTest):

    def test_deserialize_phone_number(self):
        phone_number_data = {
            'name': 'Test Phone Number',
            'phone_number': '123456789',
        }
        serializer = PhoneNumberSerializer(data=phone_number_data, owner=self.user, alpha2_code='US')
        self.assertTrue(serializer.is_valid())
        phone_number = serializer.save()
        self.assertEqual(phone_number.name, phone_number_data['name'])
        self.assertEqual(phone_number.country, self.country)
        self.assertEqual(phone_number.phone_number, phone_number_data['phone_number'])
        self.assertEqual(phone_number.owner_person, self.user)

    def test_deserialize_phone_number_raises_value_error(self):
        phone_number_data = {
            'name': 'Test Phone Number',
            'phone_number': '123456789',
        }

        with self.assertRaises(ValueError):
            serializer = PhoneNumberSerializer(data=phone_number_data, owner=self.user)
            self.assertTrue(serializer.is_valid())
            serializer.save()

    def test_update_method(self):
        phone_number_data = {
            'name': 'Test Phone Number',
            'phone_number': '123456789',
        }
        serializer = PhoneNumberSerializer(
            data=phone_number_data, owner=self.user, alpha2_code='US', instance=self.user_phone_number)
        self.assertTrue(serializer.is_valid())
        phone_number = serializer.save()
        self.assertEqual(phone_number.name, phone_number_data['name'])
        self.assertEqual(phone_number.country, self.country)
        self.assertEqual(phone_number.phone_number, phone_number_data['phone_number'])
        self.assertEqual(phone_number.owner_person, self.user)
