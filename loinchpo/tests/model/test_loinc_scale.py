import unittest
from ddt import ddt, data, unpack
from loinchpo.model.LoincScale import LoincScale


@ddt
class LoincIdTest(unittest.TestCase):

    @data((LoincScale.QN, "qn"), (LoincScale.ORD, "ord"), (LoincScale.ORDQN, "ordqn"),
          (LoincScale.NOM, "nom"), (LoincScale.NAR, "nar"), (LoincScale.MULTI, "multi"),
          (LoincScale.DOC, "doc"), (LoincScale.SET, "set"), (LoincScale.UNKNOWN, "UNKNOWN"))
    @unpack
    def test_loinc_scale(self, enum, scale):
        self.assertEqual(enum, LoincScale.parse(scale.upper()))

    @data(("quantitative,calendar", "QN"), ("ordinal", "ORD"),
          ("quantitative,pizza, bear, ordinal", "ORDQN"),
          ("splish, splash, bath, nominal", "NOM"), ("narrative", "NAR"),
          ("cake, bake", "UNKNOWN"))
    @unpack
    def test_loinc_infer_long_name(self, long_name, expected):
        self.assertEquals(LoincScale.infer_long(long_name), expected)
