import csv
from loinchpo import Query
from loinchpo.error.LoincHpoFileValidationError import LoincHpoValidationError
from loinchpo.error.LoincHpoParsingError import LoincHpoParsingError


class QueryFileParser:
    """Provides methods for parsing query files

    """

    @staticmethod
    def parse(file_path):
        """ Parses query files to Query objects.

        Args:
            file_path: A path to a query file.

        Returns:
            A list of Query objects which have valid loinc_id and outcome values.
            [Query, Query]

        Raises:
            OSError: When the file could not be opened or found.
            LoincHpoParsingError: When there were issues with file format
            LoincValidationValidationError: When there were issues with specific field expected values.

        """
        queries = []
        try:
            with open(file_path) as f:
                reader = csv.reader(f, delimiter='\t')
                for line in reader:
                    loinc_id, outcome = line
                    queries.append(Query(loinc_id, outcome))
            return queries
        except (OSError, LoincHpoParsingError, LoincHpoValidationError) as e:
            raise e
