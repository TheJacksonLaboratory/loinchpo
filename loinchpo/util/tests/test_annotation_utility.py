import unittest
from ddt import ddt, data
from loinchpo.util.AnnotationUtility import AnnotationUtility


@ddt
class AnnotationSanityTest(unittest.TestCase):

    @data(("27365-6", True), ("5778-6", True), ("16110-9", True), ("adfdf-oool", False),
          ("", False), (None, False))
    def test_loinc_id(self, item):
        self.assertEqual(AnnotationUtility.is_loinc_id(item[0]), item[1])

    @data(("NEG", True), ("POS", True), ("H", True), ("X", False),
          ("", False), (None, False))
    def test_measure(self, item):
        self.assertEqual(AnnotationUtility.is_measure(item[0]), item[1])
