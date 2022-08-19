import pyspark.sql.functions as F


class Cleaner:
    @staticmethod
    def impute_measurement_values(df):
        """As indicated by the OMOP CDM, make sure that all negative values coming from the source, set the value_as_number to NULL,
        with the exception of the following Measurements:
            - 3003396 (Base excess in Arterial blood by calculation)
            - 3002032 (Base excess in Venous blood by calculation)
            - 3006277 (QRS-Axis), 3012501 (Base excess in Blood by calculation)
            - 3003129 (Base excess in Capillary blood by calculation)
            - 3004959 (Base excess in Arterial cord blood by calculation)
            - 3007435 (Base excess in Venous cord blood by calculation)
        """

        concept_list = [3003396, 3002032, 3006277, 3012501, 3003129, 3004959, 3007435]
        updated_values = df.withColumn("value_as_number",
                                       F.when((df.value_as_number < 0.0) & (~df.concept_id.isin(concept_list)),
                                              None).otherwise(df.value_as_number))

        return updated_values
