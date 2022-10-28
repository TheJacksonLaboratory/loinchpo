import unittest

from ddt import ddt
from pyspark.sql import SparkSession

from loinchpo.core.ConceptSynonymTransformer import ConceptSynonymTransformer
from loinchpo.core.MeasurementTransformer import MeasurementTransformer
from loinchpo.tests.core.transformer_data import get_measurement_df, get_concept_synonym_df, get_concept_df


@ddt
class ConceptSynonymTransformerTest(unittest.TestCase):
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

    def test_transform(self):
        m = MeasurementTransformer()
        df = m.transform(get_measurement_df(self.spark), get_concept_df(self.spark))
        t = ConceptSynonymTransformer()
        df = t.transform(df, get_concept_df(self.spark), get_concept_synonym_df(self.spark))
        self.assertEquals(df.where(df.concept_id == 1).first()["synonym_list"], "glucosis,bloody iron")

