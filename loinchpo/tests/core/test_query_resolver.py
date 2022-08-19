import os
import unittest
from ddt import ddt, data
from loinchpo.io.AnnotationParser import AnnotationParser
from loinchpo.core.QueryResolver import QueryResolver
from loinchpo.model.Query import Query

@ddt
class AnnotationResolverTest(unittest.TestCase):

    @data(("2823-3", "N", "HP:0011042"),
          ("2823-3", "H", "HP:0011042"),
          ("5803-2", "H", "HP:0032369"),
          ("2091-7", "H", "HP:0003362"),
          ("2091-7", "N", ""))
    def test_loinc_id(self, expected):
        test_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 '../io/test_annotation_file.tsv')
        annotations = AnnotationParser.parse_annotation_file(test_file)
        resolver = QueryResolver(annotations)
        query = Query(expected[0], expected[1])
        self.assertEqual(resolver.resolve(query),
                         expected[2])

