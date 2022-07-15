import pandas as pd
from loinchpo.model.ClinicalTableName import ClinicalTableName
from loinchpo.error.ClinicalParsingError import ClinicalParsingError


class ClinicalTableParser:
    __CLINICAL_MEASUREMENT_COLUMNS = ['measurement_id', 'measurement_concept_id', 'person_id', 'visit_occurrence_id',
                                      'measurement_date', 'value_as_number', 'range_high', 'range_low']
    __CLINICAL_CONCEPT_COLUMNS = []
    __CLINICAL_CONCEPT_SYNONYM_COLUMNS = []
    __CLINICAL_VOCABULARY_COLUMNS = []

    def parse_table(self, data, table_name: ClinicalTableName):
        if isinstance(data, pd.DataFrame):
            # Does it look like what we expect?
            if ClinicalTableParser._required_columns_exist(data.columns, table_name):
                return data
        elif isinstance(data, str):
            # try to parse as csv
            try:
                df = pd.read_csv(data, header=0, low_memory=False)
                if not self._required_columns_exist(df.columns, table_name):
                    raise ClinicalParsingError(
                        "Some input columns %s are missing from required columns %s ".format(df.columns,
                                                                                             self._get_required_columns(
                                                                                                 table_name))
                    )
                return df
            except pd.errors.ParseError:
                try:
                    df = pd.read_csv(data, header=0, sep='\t', low_memory=False)
                    if not self._required_columns_exist(df.columns, table_name):
                        raise ClinicalParsingError(
                            "Some input columns %s are missing from required columns %s ".format(
                                df.columns, self._get_required_columns(table_name))

                        )
                    return df
                except pd.errors.ParseError:
                    raise ClinicalParsingError(
                        "Error parsing clinical file, must be either path to delimited file or pandas dataframe.")

    def _required_columns_exist(self, input_columns, table_name):
        """
            Take input columns and table_name and returns whether we have the required columns to do our transform

            Args:
                input_columns: the columns of our input table
                table_name: A ClinicalTableName enum of the table

            Returns:
                Boolean of whether the required columns exist.
        """

        required_columns = self._get_required_columns(table_name)
        return all(x.lower in required_columns for x in input_columns)

    def _get_required_columns(self, table_name):
        if table_name == ClinicalTableName.MEASUREMENT:
            return self.__CLINICAL_MEASUREMENT_COLUMNS
        elif table_name == ClinicalTableName.CONCEPT:
            return self.__CLINICAL_CONCEPT_COLUMNS
        elif table_name == ClinicalTableName.CONCEPT_SYNONYM:
            return self.__CLINICAL_CONCEPT_SYNONYM_COLUMNS
        elif table_name == ClinicalTableName.VOCABULARY:
            return self.__CLINICAL_VOCABULARY_COLUMNS
