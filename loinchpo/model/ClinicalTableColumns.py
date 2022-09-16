from loinchpo import ClinicalTableName


class ClinicalTableColumns:

    @staticmethod
    def get(table_name: ClinicalTableName):
        """
            Gets the required columns based on the ::class::`ClinicalTableName`.
        """
        if table_name == ClinicalTableName.MEASUREMENT:
            return ['measurement_id', 'measurement_concept_id', 'person_id', 'visit_occurrence_id',
                    'measurement_date', 'value_as_number', 'range_low', 'range_high']
        elif table_name == ClinicalTableName.CONCEPT:
            return ['concept_id', 'concept_code', 'concept_name', 'vocabulary_id', 'concept_class_id',
                    'domain_id', 'invalid_reason']
        elif table_name == ClinicalTableName.CONCEPT_SYNONYM:
            return ['concept_id', 'concept_synonym_name']
        elif table_name == ClinicalTableName.VOCABULARY:
            return ['vocabulary_version', 'vocabulary_id']

    @staticmethod
    def get_mutually_exclusive(table_name: ClinicalTableName):
        if table_name == ClinicalTableName.MEASUREMENT:
            return ['value_as_concept_id', 'value_as_concept_name']
        return []
