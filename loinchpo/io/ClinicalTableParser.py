import pyspark.sql.dataframe

from loinchpo.model.ClinicalTableColumns import ClinicalTableColumns
from loinchpo import ClinicalTableName
from loinchpo.error.ClinicalParsingError import ClinicalParsingError


class ClinicalTableParser:
    """ Provides methods for parsing OMOP clinical tables.

        Example:
            parser = ClinicalTableParser()
            parser.parse_table("/some/file/path", ClinicalTableName.CONCEPT, your_context)

    """
    def parse_table(self, path, table_name: ClinicalTableName, spark_session: pyspark.sql.SparkSession,
                    sep=',') -> pyspark.sql.DataFrame:
        """
            Parses a OMOP table to a spark dataframe

            Args:
                path: the path to the delimited omop table file
                table_name: a :class::`ClinicalTableName` of the csv being passed
                spark_session: a valid spark session
                sep: defaults to comma the seperator for the delimited file
            Returns:
                A spark dataframe representing the OMOP Clinical Table

            Raises:
                ClinicalParsingError: If the file is not formatted correctly or is missing required columns
        """
        if isinstance(path, str) and spark_session is not None:
            try:
                df = spark_session.read.csv(path, header=True, sep=sep)
                return self.verify_table(df, table_name)
            except Exception as e:
                if isinstance(e, ClinicalParsingError):
                    raise e
                else:
                    raise ClinicalParsingError(str(e))

    def verify_table(self, df: pyspark.sql.DataFrame, table_name: ClinicalTableName):
        """
            Verifies that a pyspark OMOP dataframe has the required columns to do transformation

            Args:
                df: A ::class::`pyspark.sql.Dataframe` of an OMOP table
                table_name: the name of the OMOP table for the dataframe
            Returns:
                The spark dataframe
            Raises:
                ClinicalParsingError: if the required columns are missing

        """
        if isinstance(df, pyspark.sql.dataframe.DataFrame):
            if self._required_columns_exist(df.columns, table_name):
                return df
            else:
                raise ClinicalParsingError(
                    "Some input columns %s are missing from required columns %s ".format(list(df.columns),
                                                                                         ClinicalTableColumns.get(
                                                                                             table_name))
                )

    def _required_columns_exist(self, input_columns, table_name):
        """
            Take input columns and table_name and returns whether we have the required columns to do our transform

            Args:
                input_columns: the columns of our input table
                table_name: A ClinicalTableName enum of the table

            Returns:
                Boolean of whether the required columns exist.
        """
        input_columns = [x.lower() for x in list(input_columns)]
        required_columns = ClinicalTableColumns.get(table_name)
        mutually_exclusive = ClinicalTableColumns.get_mutually_exclusive(table_name)
        if len(mutually_exclusive) > 0:
            return all(x in input_columns for x in required_columns) and any(x in input_columns for x in mutually_exclusive)
        return all(x in input_columns for x in required_columns)
