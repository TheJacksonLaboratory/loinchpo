import unittest
from ddt import ddt
from pyspark.sql import SparkSession

from loinchpo import ClinicalTableName
from loinchpo.core.MeasurementTransformer import MeasurementTransformer
from loinchpo.model.ClinicalTableColumns import ClinicalTableColumns

# TODO: make this test more direct
@ddt
class MeasurementTransformerTest(unittest.TestCase):
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

    def test_measurement_transform_concept_name(self):
        t = MeasurementTransformer()
        df = t.transform(self.get_measurement_df(), self.get_concept_df())
        self.assertEquals(df.count(), 3)

    def test_measurement_transform_concept_id(self):
        t = MeasurementTransformer()
        df = t.transform(self.get_measurement_df_id(), self.get_concept_df())
        self.assertEquals(df.count(), 3)

    def _get_measurement_cols_name(self):
        return ['measurement_id', 'measurement_concept_id', 'person_id', 'visit_occurrence_id',
                'measurement_date', 'value_as_number', 'value_as_concept_name', 'range_low', 'range_high']

    def _get_measurement_cols_id(self):
        return ['measurement_id', 'measurement_concept_id', 'person_id', 'visit_occurrence_id',
                'measurement_date', 'value_as_number', 'value_as_concept_id', 'range_low', 'range_high']

    def get_measurement_df(self):
        # normal -> loinc result high with good numbers
        # categorical with positive indicator
        # categorical with negative indicator
        # missing should be imputed
        # range high is less than range low no mapping
        # range low is missing no mapping
        return self.spark.createDataFrame([
            (1, 1, 3092, 1, "10/30/2006", float(85), None, 60, 75),
            (2, 2, 3092, 1, "10/27/2007", None, "positive", None, None),
            (3, 2, 3092, 1, "10/27/2008", None, "normal", None, None),
            (4, 4, 3092, 1, "11/28/2008", None, None, None, None),
            (5, 5, 3092, 1, "11/28/2008", float(60.6), None, 50, 30),
            (6, 5, 3092, 1, "11/28/2008", float(30), None, None, 29),
            (7, 8, 3092, 1, "10/27/2007", None, "positive", None, None),
        ], self._get_measurement_cols())

    def get_measurement_df_id(self):
        return self.spark.createDataFrame([
            (1, 1, 3092, 1, "10/30/2006", float(85), None, 60, 75),
            (2, 2, 3092, 1, "10/27/2007", None, 7, None, None),
            (3, 2, 3092, 1, "10/27/2008", None, 8, None, None),
            (4, 4, 3092, 1, "11/28/2008", None, None, None, None),
            (5, 5, 3092, 1, "11/28/2008", float(60.6), None, 50, 30),
            (6, 5, 3092, 1, "11/28/2008", float(30), None, None, 29),
            (7, 9, 3092, 1, "10/27/2007", None, 8, None, None),
        ], self._get_measurement_cols_id())

    def _get_concept_cols(self):
        return ClinicalTableColumns.get(ClinicalTableName.CONCEPT)

    def get_concept_df(self):
        return self.spark.createDataFrame([
            (1, 203, "Glucose in Serum", "LOINC", 30, "Measurement", None),
            (2, 204, "Abnormal Lung Structure", "LOINC", 31, "Measurement", None),
            (4, 205, "Iron in Blood g/Mg", "LOINC", 33, "Measurement", None),
            (5, 206, "Some fake rxnorm", "RxNorm", 34, "Measurement", None),
            (6, 207, "Some fake snowmed", "SNOWMED", 35, "Measurement", "null"),
            (7, 209, "Positive", "LOINC", 26, "Measurement Value", None),
            (8, 210, "Normal", "LOINC", 27, "Measurement Value", None)
            ], self._get_concept_cols())


