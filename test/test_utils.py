from unittest import TestCase

from oireachtas_nlp.utils import flatten


class UtilsTest(TestCase):
    def test_flatten(self):
        self.assertEqual(flatten([[1, 2, 3], [1, 2]]), [1, 2, 3, 1, 2])
