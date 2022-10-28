from pyspark import F

from loinchpo.core.ConceptSynonymTransformer import ConceptSynonymTransformer
from loinchpo.core.MeasurementTransformer import MeasurementTransformer
from loinchpo.model.LoincScale import LoincScale


class OMOPTransformer:

    @staticmethod
    def transform(measurement_table, concept_table, concept_synonym_table):
        m = MeasurementTransformer()
        df = m.transform(measurement_table, concept_table)
        s = ConceptSynonymTransformer()
        df = s.transform(df, concept_table, concept_synonym_table)
        loinc_scale_udf = F.udf(lambda x: LoincScale.infer_long(x))
        df = df.select("*", loinc_scale_udf("synonym_list").alias("loinc_scale_type")).dropDuplicates()
        return df.select("person_id", "visit_occurrence_id", "measurement_id",
                         "measurement_date", "concept_id", "concept_code", "concept_name", "loinc_result",
                         "loinc_scale_type", "value_as_concept_name", "value_as_number", "range_low", "range_high")
