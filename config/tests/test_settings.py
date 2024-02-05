from django.core.exceptions import ImproperlyConfigured
from django.test import SimpleTestCase

from ..settings import get_env_variable


class SettingsTest(SimpleTestCase):

    def test_get_env_variable_raises_exception(self):
        env_variable = 'NOT_EXISTING_ENV_VAR'
        exception_message = f'Set the {env_variable} environment variable'
        with self.assertRaisesMessage(ImproperlyConfigured, exception_message):
            get_env_variable(env_variable)
