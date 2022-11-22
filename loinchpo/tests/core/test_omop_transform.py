import unittest

from ddt import ddt
from pyspark.sql import SparkSession

from loinchpo.core.OMOPTransformer import OMOPTransformer
from loinchpo.tests.core.transformer_data import get_measurement_df, get_concept_synonym_df, get_concept_df

@ddt
class TestOMOPTransform(unittest.TestCase):
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


    def test_full_transform(self):
        transformed = OMOPTransformer.transform(get_measurement_df(self.spark), get_concept_df(self.spark),
                                                   get_concept_synonym_df(self.spark))
        self.assertEqual(transformed.count(), 3)

