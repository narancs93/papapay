from django.test import SimpleTestCase

from ...common.utils import remove_prefix


class UtilsTest(SimpleTestCase):

    def test_remove_prefix_removes_prefix(self):
        actual = remove_prefix('+36 201234567', '+36')
        expected = ' 201234567'

        self.assertEqual(expected, actual)

    def test_remove_prefix_returns_original_string_without_prefix(self):
        actual = remove_prefix('201234567', '+36')
        expected = '201234567'

        self.assertEqual(expected, actual)
