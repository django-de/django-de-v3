from django.test import TestCase

from . import utils


class UtilsTests(TestCase):
    def test_is_prerelease(self):
        self.assertTrue(utils.is_prerelease("1.2a3"))
        self.assertFalse(utils.is_prerelease("1.2"))
