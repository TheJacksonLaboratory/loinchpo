import os
import unittest
import warnings

from ddt import ddt, data, unpack
from pyspark.sql import SparkSession

from loinchpo import ClinicalTableName
from loinchpo import ClinicalTableParser


@ddt
class ClinicalTableParserTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings("ignore", category=ResourceWarning)
        cls.spark = (SparkSession
                     .builder
                     .master("local[*]")
                     .appName("Unit-tests")
                     .getOrCreate())
        cls.spark.sparkContext.setLogLevel("ERROR")
    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()
        cls.spark.sparkContext.stop()

    @data(
        ("concept", ClinicalTableName.CONCEPT),
        ("concept_synonym", ClinicalTableName.CONCEPT_SYNONYM),
        ("measurement", ClinicalTableName.MEASUREMENT),
        ("vocabulary", ClinicalTableName.VOCABULARY)
    )
    @unpack
    def test_clinical_table_parser(self, file_name, table_name):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '{0}.csv'.format(file_name))
        parser = ClinicalTableParser()
        self.assertFalse(parser.parse_table(file_path, table_name, self.spark).first() is None)
