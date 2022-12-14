from loinchpo import ClinicalTableName
from loinchpo.model.ClinicalTableColumns import ClinicalTableColumns


def _get_measurement_cols_name():
    return ['measurement_id', 'measurement_concept_id', 'person_id', 'visit_occurrence_id',
            'measurement_date', 'value_as_number', 'value_as_concept_name', 'range_low', 'range_high']

def _get_measurement_cols_id():
    return ['measurement_id', 'measurement_concept_id', 'person_id', 'visit_occurrence_id',
            'measurement_date', 'value_as_number', 'value_as_concept_id', 'range_low', 'range_high']

def get_measurement_df(spark):
    # normal -> loinc result high with good numbers
    # categorical with positive indicator
    # categorical with negative indicator
    # missing should be imputed
    # range high is less than range low no mapping
    # range low is missing no mapping
    return spark.createDataFrame([
        (1, 1, 3092, 1, "10/30/2006", float(85), None, 60, 75),
        (2, 2, 3092, 1, "10/27/2007", None, "positive", None, None),
        (3, 2, 3092, 1, "10/27/2008", None, "normal", None, None),
        (4, 4, 3092, 1, "11/28/2008", None, None, None, None),
        (5, 5, 3092, 1, "11/28/2008", float(60.6), None, 50, 30),
        (6, 5, 3092, 1, "11/28/2008", float(30), None, None, 29),
        (7, 8, 3092, 1, "10/27/2007", None, "positive", None, None),
    ], _get_measurement_cols_name())

def get_measurement_df_id(spark):
    return spark.createDataFrame([
        (1, 1, 3092, 1, "10/30/2006", float(85), None, 60, 75),
        (2, 2, 3092, 1, "10/27/2007", None, 7, None, None),
        (3, 2, 3092, 1, "10/27/2008", None, 8, None, None),
        (4, 4, 3092, 1, "11/28/2008", None, None, None, None),
        (5, 5, 3092, 1, "11/28/2008", float(60.6), None, 50, 30),
        (6, 5, 3092, 1, "11/28/2008", float(30), None, None, 29),
        (7, 9, 3092, 1, "10/27/2007", None, 8, None, None),
    ], _get_measurement_cols_id())

def _get_concept_cols():
    return ClinicalTableColumns.get(ClinicalTableName.CONCEPT)

def get_concept_df(spark):
    return spark.createDataFrame([
        (1, 203, "Glucose in Serum", "LOINC", 30, "Measurement", None),
        (2, 204, "Abnormal Lung Structure", "LOINC", 31, "Measurement", None),
        (4, 205, "Iron in Blood g/Mg", "LOINC", 33, "Measurement", None),
        (5, 206, "Some fake rxnorm", "RxNorm", 34, "Measurement", None),
        (6, 207, "Some fake snowmed", "SNOWMED", 35, "Measurement", "null"),
        (7, 209, "Positive", "LOINC", 26, "Measurement Value", None),
        (8, 210, "Normal", "LOINC", 27, "Measurement Value", None),
        (1001, 211, "English Language", "SnowMed", 28, "Qualifier Value", None),
        (1002, 212, "German Language", "SnowMed", 29, "Qualifier Value", None)
    ], _get_concept_cols())

def get_concept_synonym_columns():
    return ClinicalTableColumns.get(ClinicalTableName.CONCEPT_SYNONYM) + ["language_concept_id"]

def get_concept_synonym_df(spark):
    return spark.createDataFrame([
        (1, "glucosis", 1001),
        (1, "ordinal", 1001),
        (1, "bloody iron", 1001),
        (2, "haus", 1002),
        (2, "quantitative", 1001)
    ], get_concept_synonym_columns())
