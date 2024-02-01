from django.core.exceptions import ValidationError

from ....common.tests.base_setup_test import BaseSetupTest
from ....postal_address.models import City


class CityTest(BaseSetupTest):
    def test_create_and_save_model(self):
        city = City(name='Test City', state=self.state)
        city.save()

        saved_city = City.objects.get(id=city.id)
        self.assertEqual(saved_city.name, 'Test City')
        self.assertEqual(saved_city.state, self.state)

    def test_unique_name_and_state_together_is_enforced(self):
        with self.assertRaises(ValidationError):
            City.objects.create(name='Example City', state=self.state)

    def test_name_mandatory_is_enforced(self):
        with self.assertRaises(ValidationError):
            City.objects.create(state=self.state)

    def test_state_mandatory_is_enforced(self):
        with self.assertRaises(ValidationError):
            City.objects.create(name='City without State')

    def test_str(self):
        expected = f'Example City (Example State) (id={self.city.id})'
        actual = str(self.city)

        self.assertEqual(expected, actual)
