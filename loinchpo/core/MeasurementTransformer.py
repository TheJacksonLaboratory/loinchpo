from loinchpo import ClinicalTableName
from loinchpo.core.Cleaner import Cleaner
import pyspark.sql.functions as F
from pyspark.sql.functions import coalesce

from loinchpo.error.ClinicalParsingError import ClinicalParsingError
from loinchpo.io.clinical.ClinicalTableParser import ClinicalTableParser


class MeasurementTransformer:

    def __init__(self):
        self.postive_category_indicators = ["positive", "detected", "abnormal", "yes"]
        self.negative_category_indicators = ["negative", "not detected", "normal", "acceptable", "healthy", "in range",
                                             "non-reactive", "nonreactive", "none detected", "none seen",
                                             "not detected/negative", "not present", "no"]

    def transform(self, measurement_table, concept_table):
        """
            We want to interpret measurement values to high low normal
            based on reference ranges and gather other values.

            Args:
                measurement_table: the measurement table dataframe
                concept_table: the concept table dataframe
                concept_synonym_table: the concept synonym dataframe
        """
        try:
            parser = ClinicalTableParser()
            parser.verify_table(measurement_table, ClinicalTableName.MEASUREMENT)
            parser.verify_table(concept_table, ClinicalTableName.CONCEPT)
        except ClinicalParsingError as e:
            print(str(e))
            exit(2)

        clean_df = self._process_measurement(measurement_table, concept_table)
        clean_df = self._obtain_loinc_results(clean_df)
        return clean_df

    def _process_measurement(self, measurement_table, concept_table):
        """Filters the measurement table to only include loinc measurements with a result"""

        loinc_concept_table = concept_table.filter((concept_table.domain_id == "Measurement") &
                                             (concept_table.vocabulary_id == "LOINC") &
                                             (concept_table.invalid_reason.isNull()))
        correct_measurement_val_col = "value_as_concept_name"
        correct_measurement_val_col = "value_as_concept_id" if "value_as_concept_name" not in measurement_table.columns else correct_measurement_val_col

        # Get measurement concept
        merged = measurement_table.withColumnRenamed("measurement_concept_id", "concept_id").filter(
            coalesce("value_as_number", correct_measurement_val_col).isNotNull()).join(loinc_concept_table, ["concept_id"])

        # Figure out if we already have the column ( n3c auto joined these)
        if correct_measurement_val_col == "value_as_concept_id":
            # Get value as concept name
            value_concept = merged.select("value_as_concept_id").dropDuplicates()
            value_concept = value_concept.join(concept_table, value_concept.value_as_concept_id == concept_table.concept_id,
                                               "left").select("value_as_concept_id", "concept_name").withColumnRenamed(
                "concept_name", "value_as_concept_name")
            merged = merged.join(value_concept, "value_as_concept_id", "left")

        # remove invalid concepts that are not loinc measurements
        merged = merged.select("person_id", "visit_occurrence_id",
                               "measurement_id", "measurement_date", "concept_id",
                               "concept_code", "concept_name", "value_as_concept_name",
                               "value_as_number", "range_high", "range_low").dropDuplicates()

        # cast numeric columns to double
        merged = merged.withColumn("value_as_number", F.col("value_as_number").cast("double"))
        merged = merged.withColumn("range_low", F.col("range_low").cast("double"))
        merged = merged.withColumn("range_high", F.col("range_high").cast("double"))
        # verify proper handling of negative value_source_value
        return Cleaner.impute_measurement_values(merged)

    def _obtain_loinc_results(self, df):
        """
            Obtains the result of measurement and reference ranges

            Args:
                A cleaned measurement concept table of loinc values.
        """
        helper_function = F.udf(lambda x: self._infer_result(x[0], x[1], x[2], x[3]))
        input_columns = F.struct("value_as_concept_name", "value_as_number", "range_low", "range_high")
        return df.select("*", helper_function(input_columns).alias("loinc_result")).dropDuplicates()

    def _infer_result(self, value_as_concept_name, value_as_number, range_low, range_high):
        """Helper function that parses and returns the loinc result based on a reference range"""

        # Determine if a concept is numerical or categorical and check result.
        if value_as_concept_name is not None and value_as_number is None:
            if value_as_concept_name != "No matching concept":
                temp_result = self._checks_categorical_result_value(value_as_concept_name)
                if temp_result is not None:
                    result = temp_result
                else:
                    result = "Categorical result not a Current Mapped Type and numeric result value is Missing"
            else:
                result = "Categorical Result has value 'No matching concept' and numeric result value is Missing"
        elif value_as_concept_name is not None and value_as_number is not None:
            if value_as_concept_name != "No matching concept":
                temp_result = self._checks_categorical_result_value(value_as_concept_name)
                if temp_result is not None:
                    result = temp_result
                else:
                    result = self._checks_numeric_result_value(value_as_number, range_low, range_high)
            else:
                temp_result = self._checks_numeric_result_value(value_as_number, range_low, range_high)
                if temp_result == "missing both range_low and range_high values":
                    result = "Categorical Result has value 'No matching concept' and reference range values are missing"
                else:
                    result = temp_result
        elif value_as_concept_name is None and value_as_number is not None:
            result = self._checks_numeric_result_value(value_as_number, range_low, range_high)
        else:
            result = "Categorical Result is missing and numeric result is missing"

        return result

    def _checks_categorical_result_value(self, value_as_concept_name):
        """
            Verifies values for a categorical result from the value_as_concept_name column
        """

        if value_as_concept_name.lower() in self.postive_category_indicators + self.negative_category_indicators:
            if value_as_concept_name.lower() in self.postive_category_indicators:
                result = "positive"
            else:
                result = "negative"
        else:
            result = None
        return result

    def _checks_numeric_result_value(self, value_as_number, range_low, range_high):
        """Verifies values for a numeric result from the value_as_number column"""

        if range_low is not None and range_high is not None:
            if range_low != 0.0 and range_high != 0.0:
                if range_low < range_high:
                    if value_as_number < range_low:
                        result = "low"
                    elif value_as_number > range_high:
                        result = "high"
                    else:
                        result = "normal"
                elif range_low > range_high:
                    result = "range_low value > range_high value"
                else:
                    result = "range_low value == range_high value"
            elif range_low != 0.0 and range_high == 0.0:
                result = "range_high value == zero, but range_low value != 0"
            elif range_low == 0.0 and range_high != 0.0:
                result = "range_low value == zero, but range_high value != 0"
            else:
                result = "Both range_low and range_high values are zero"
        elif range_low is None and range_high is not None:
            result = "missing range_low value, but not missing range_high value"
        elif range_low is not None and range_high is None:
            result = "missing range_high value, but not missing range_low value"
        else:
            result = "missing both range_low and range_high values"
        return result
