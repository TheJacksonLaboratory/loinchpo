import unittest
from ddt import ddt, data, unpack
from loinchpo.models.LoincId import LoincId
from loinchpo.errors.SeepParsingError import SeepParsingError


@ddt
class LoincIdTest(unittest.TestCase):

    @data(("999-1", "999", "1"), ("1999-2", "1999", "2"), ("5792-7", "5792", "7"))
    @unpack
    def test_loincId_pass(self, code, num, suffix):
        res = LoincId(code)
        self.assertEqual(res.loinc_id, code)
        self.assertEqual(res.num, num)
        self.assertEqual(res.suffix, suffix)

    @data("9991", "999:d", None)
    def test_loincId_fail(self, code):
        self.assertRaises(SeepParsingError, LoincId, code)


