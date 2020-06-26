import os
import unittest
from ddt import ddt, data
from loinchpo.util.AnnotationParser import AnnotationParser
from loinchpo.util.AnnotationResolver import AnnotationResolver
from loinchpo.models.Query import Query

@ddt
class AnnotationResolverTest(unittest.TestCase):

    @data(("2823-3", "N", "true", "HP:0011042"),
          ("2823-3", "H", "true", "HP:0011042"),
          ("5803-2", "H", "false", "HP:0032369"),
          ("2091-7", "H", "false", "HP:0003362"),
          ("2091-7", "N", "false", ""))
    def test_loinc_id(self, expected):
        test_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 'test_annotation_file.tsv')
        annotations = AnnotationParser.parse_annotation_file_dict(test_file)
        resolver = AnnotationResolver(annotations)
        query = Query(expected[0], expected[1], expected[2])
        self.assertEqual(resolver.resolve(query),
                         expected[3])

