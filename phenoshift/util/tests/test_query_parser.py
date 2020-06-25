import unittest
import os
from ddt import ddt, data
from phenoshift.util.QueryFileParser import QueryFileParser


@ddt
class QueryParserTest(unittest.TestCase):

    # Expectation data after parse
    @data((
            ("2823-3", "H", "true", True),
            ("2823-3", "N", "true", True),
            ("2091-7", "H", "false", False)
    ))
    def test_query_parser(self, expected_data):
        test_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_query.tsv')
        queries = QueryFileParser.parse(test_file)
        for query, expected in zip(queries, expected_data):
            self.assertEqual(query.loinc_id, expected[0])
            self.assertEqual(query.measure, expected[1])
            self.assertEqual(query.negated, expected[3])
