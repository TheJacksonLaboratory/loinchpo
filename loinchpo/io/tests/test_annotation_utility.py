import unittest
from ddt import ddt, data
from loinchpo.io.Utility import Utility


@ddt
class AnnotationSanityTest(unittest.TestCase):

    @data(("27365-6", True), ("5778-6", True), ("16110-9", True), ("adfdf-oool", False),
          ("", False), (None, False))
    def test_loinc_id(self, item):
        self.assertEqual(Utility.is_loinc_id(item[0]), item[1])

    @data(("NEG", True), ("POS", True), ("H", True), ("X", False),
          ("", False), (None, False))
    def test_outomce(self, item):
        self.assertEqual(Utility.is_outcome(item[0]), item[1])

    @data(("NEGATIVE", "NEG"), ("POSITIVE", "POS"), ("HIGH", "H"), ("LOW", "L"), ("NORMAL", "N"))
    def test_outcome_parse(self, item):
        self.assertEqual(Utility.parse_outcome(item[0]), item[1])
