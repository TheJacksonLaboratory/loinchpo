import unittest
from ddt import ddt
from pyspark.sql import SparkSession

from loinchpo import ClinicalTableName
from loinchpo.model.ClinicalTableColumns import ClinicalTableColumns


@ddt
class ConceptTransformerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.spark = (SparkSession
                     .builder
                     .master("local[*]")
                     .appName("Unit-tests")
                     .getOrCreate())

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()


    def test_concept_transformer(self):
        pass

    def get_concept_columns(self):
        return ClinicalTableColumns.get(ClinicalTableName.CONCEPT)

    def get_concept_df(self):
        return self.spark.createDataFrame([

        ], self.get_concept_columns())

    def get_vocabulary_columns(self):
        return ClinicalTableColumns.get(ClinicalTableName.VOCABULARY)

    def get_vocabulary_df(self):
        return self.spark.createDataFrame([
            ()
        ], self.get_vocabulary_columns())
