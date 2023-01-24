import unittest
import warnings

from ddt import ddt
from pyspark.sql import SparkSession

from loinchpo import ConceptSynonymTransformer
from loinchpo import MeasurementTransformer
from .transformer_data import get_measurement_df, get_concept_synonym_df, get_concept_df


@ddt
class ConceptSynonymTransformerTest(unittest.TestCase):
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
        cls.spark.sparkContext.stop()
        cls.spark.stop()

    def test_transform(self):
        m = MeasurementTransformer()
        df = m.transform(get_measurement_df(self.spark), get_concept_df(self.spark))
        t = ConceptSynonymTransformer()
        df = t.transform(df, get_concept_df(self.spark), get_concept_synonym_df(self.spark))
        self.assertEqual(df.where(df.concept_id == 1).first()["synonym_list"], "glucosis,ordinal,bloody iron")

