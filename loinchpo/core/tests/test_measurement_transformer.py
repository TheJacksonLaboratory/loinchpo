import unittest
from ddt import ddt
from pyspark.sql import SparkSession
from loinchpo import MeasurementTransformer

# TODO: make this test more direct
from loinchpo.core.tests.transformer_data import get_measurement_df, get_concept_df, \
    get_measurement_df_id


@ddt
class MeasurementTransformerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spark = (SparkSession
                     .builder
                     .master("local[*]")
                     .appName("Unit-tests")
                     .getOrCreate())
        cls.spark.sparkContext.setLogLevel("ERROR")

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()

    def test_omop_transform_concept_name(self):
        t = MeasurementTransformer()
        df = t.transform(get_measurement_df(self.spark), get_concept_df(self.spark))
        self.assertEqual(df.count(), 3)

    def test_omop_transform_concept_id(self):
        t = MeasurementTransformer()
        df = t.transform(get_measurement_df_id(self.spark), get_concept_df(self.spark))
        self.assertEqual(df.count(), 3)


