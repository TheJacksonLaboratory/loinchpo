import csv
from loinchpo.models.Query import Query
from loinchpo.errors.SeepValidationError import SeepValidationError
from loinchpo.errors.SeepParsingError import SeepParsingError


class QueryFileParser:
    """Provides methods for parsing query files

    """

    @staticmethod
    def parse(file_path):
        """ Parses query files to Query objects.

        Args:
            file_path: A path to a query file.

        Returns:
            A list of Query objects which have valid loinc_id, measure and negation values.
            [Query, Query]

        Raises:
            OSError: When the file could not be opened or found.
            SeepParsingError: When there were issues with file format
            SeepValidationError: When there were issues with specific field expected values.

        """
        queries = []
        try:
            with open(file_path) as f:
                reader = csv.reader(f, delimiter='\t')
                for line in reader:
                    loinc_id, measure, negated = line
                    queries.append(Query(loinc_id, measure, negated))
            return queries
        except (OSError,  SeepParsingError, SeepValidationError) as e:
            raise e
