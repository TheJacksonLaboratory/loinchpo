import os
import unittest
from ddt import ddt, data, unpack

from loinchpo import ClinicalTableName
from loinchpo.io.clinical.ClinicalTableParser import ClinicalTableParser


@ddt
class ClinicalTableParserTest(unittest.TestCase):

    @data(
        ("concept", ClinicalTableName.CONCEPT),
        ("concept_synonym", ClinicalTableName.CONCEPT_SYNONYM),
        ("measurement", ClinicalTableName.MEASUREMENT),
        ("vocabulary", ClinicalTableName.VOCABULARY)
    )
    @unpack
    def test_clinical_table_parser(self, file_name, table_name):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '{0}.csv'.format(file_name))
        self.assertFalse(ClinicalTableParser().parse_table(file_path, table_name).empty)
