from django.contrib.auth import get_user_model

from papapay.common.tests.base_setup_test import BaseSetupTest
from papapay.user.serializers import (PhoneNumberChoice,
                                      PhoneNumbersChoiceField,
                                      UserProfileSerializer)

User = get_user_model()


class UserProfileSerializerTest(BaseSetupTest):

    def test_serialize_user(self):
        user_data = {
            'first_name': 'Example',
            'last_name': 'User',
            'email': 'example.user@example.com',
        }
        serializer = UserProfileSerializer(data=user_data)
        serializer.is_valid()
        expected_phone_numbers = ['Example Phone Number for Example User (+1 1234556787)']
        actual_phone_numbers = list(str(choice) for choice in serializer.fields['phone_numbers'].choices)
        expected_data = {
            'first_name': 'Example',
            'last_name': 'User',
            'email': 'example.user@example.com',
            'phone_numbers': None,
        }
        self.assertEqual(serializer.data, expected_data)
        self.assertEqual(actual_phone_numbers, expected_phone_numbers)

    def test_deserialize_user(self):
        user_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test.user@example.com',
        }
        serializer = UserProfileSerializer(data=user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.first_name, user_data['first_name'])
        self.assertEqual(user.last_name, user_data['last_name'])
        self.assertEqual(user.email, user_data['email'])


class PhoneNumberChoiceTest(BaseSetupTest):

    def test_to_internal_value(self):
        phone_number_choice_field = PhoneNumbersChoiceField(choices=[PhoneNumberChoice(self.phone_number)])
        actual_phone_number = phone_number_choice_field.to_internal_value(data=[self.phone_number.id])
        expected_phone_number = {self.phone_number}

        self.assertEquals(actual_phone_number, expected_phone_number)

    def test_to_internal_value_with_phone_number_not_in_choices(self):
        phone_number_choice_field = PhoneNumbersChoiceField(choices=[PhoneNumberChoice(self.phone_number)])
        actual_phone_number = phone_number_choice_field.to_internal_value(data=[9999])
        expected_phone_number = set()

        self.assertEquals(actual_phone_number, expected_phone_number)
