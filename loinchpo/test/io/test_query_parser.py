import unittest
import os
from ddt import ddt, data
from loinchpo import QueryFileParser


@ddt
class QueryParserTest(unittest.TestCase):

    # Expectation data after parse
    @data((
            ("2823-3", "H"),
            ("2823-3", "N"),
            ("2091-7", "H")
    ))
    def test_query_parser(self, expected_data):
        test_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_query.tsv')
        queries = QueryFileParser.parse(test_file)
        for query, expected in zip(queries, expected_data):
            self.assertEqual(query.loinc_id, expected[0])
            self.assertEqual(query.outcome, expected[1])
