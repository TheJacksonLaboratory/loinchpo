import csv
from seep_hpo.models.Query import Query


class QueryFileParser:

    @staticmethod
    def parse(file_path):
        queries = []
        try:
            with open(file_path) as f:
                reader = csv.reader(f, delimiter='\t')
                for line in reader:
                    loinc_id, measure, negated = line
                    queries.append(Query(loinc_id, measure, negated))
            return queries
        except Exception as e:
            raise e
