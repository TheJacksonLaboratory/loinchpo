import unittest
from ddt import ddt, data, unpack
from loinchpo.model.LoincScale import LoincScale


@ddt
class LoincIdTest(unittest.TestCase):

    @data((LoincScale.QN, "qn"), (LoincScale.ORD, "ord"), (LoincScale.ORDQN, "ordqn"),
          (LoincScale.NOM, "nom"), (LoincScale.NAR, "nar"), (LoincScale.MULTI, "multi"),
          (LoincScale.DOC, "doc"), (LoincScale.SET, "set"), (LoincScale.UNKNOWN, "XD"))
    @unpack
    def test_loinc_scale(self, enum, scale):
        self.assertEqual(enum, LoincScale.parse(scale.upper()))


