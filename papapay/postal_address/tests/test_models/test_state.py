from django.core.exceptions import ValidationError

from papapay.postal_address.models import State

from papapay.common.tests.base_setup_test import BaseSetupTest


class StateTest(BaseSetupTest):
    def test_create_and_save_model(self):
        state = State(name='Test State', abbreviation='XYZ', area_code='XYZ-1', country=self.country)
        state.save()

        saved_state = State.objects.get(id=state.id)
        self.assertEqual(saved_state.name, 'Test State')
        self.assertEqual(saved_state.abbreviation, 'XYZ')
        self.assertEqual(saved_state.area_code, 'XYZ-1')
        self.assertEqual(saved_state.country, self.country)

    def test_unique_name_and_country_together_is_enforced(self):
        with self.assertRaises(ValidationError):
            State.objects.create(name='Example State', country=self.country)

    def test_name_mandatory_is_enforced(self):
        with self.assertRaises(ValidationError):
            State.objects.create(country=self.country)

    def test_country_mandatory_is_enforced(self):
        with self.assertRaises(ValidationError):
            State.objects.create(name='State without Country')

    def test_abbreviation_blank_by_default(self):
        state = State.objects.create(name='State without Abbreviation', area_code='NOIN', country=self.country)

        self.assertEqual(state.abbreviation, '')

    def test_area_code_blank_by_default(self):
        state = State.objects.create(name='State withot Area Code', abbreviation='NAC', country=self.country)

        self.assertEqual(state.area_code, '')

    def test_str(self):
        expected = f'Example State (United States of America) (id={self.state.id})'
        actual = str(self.state)

        self.assertEqual(expected, actual)
