from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

from loinchpo import ConceptSynonymTransformer
from loinchpo import MeasurementTransformer
from loinchpo import LoincScale


class OMOPTransformer:

    @staticmethod
    def transform(measurement_table, concept_table, concept_synonym_table, valid_results_only=True):
        m = MeasurementTransformer()
        df = m.transform(measurement_table, concept_table)
        s = ConceptSynonymTransformer()
        df = s.transform(df, concept_table, concept_synonym_table)
        loinc_scale_udf = udf(lambda x: LoincScale.infer_long(x), StringType())
        df = df.select("*", loinc_scale_udf("synonym_list").alias("loinc_scale_type")).dropDuplicates().select(
                         "person_id", "visit_occurrence_id", "measurement_id",
                         "measurement_date", "concept_id", "concept_code", "concept_name", "loinc_result",
                         "loinc_scale_type", "value_as_concept_name", "value_as_number", "range_low", "range_high")

        if valid_results_only:
            valid_result_values = ["positive", "negative", "low", "normal", "high"]
            return df.filter(df.loinc_result.isin(valid_result_values)).dropDuplicates()
        return df