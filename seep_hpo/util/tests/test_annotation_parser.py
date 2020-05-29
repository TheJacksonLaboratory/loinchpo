import unittest
import os
from ddt import ddt, data
from seep_hpo.util.AnnotationParser import AnnotationParser


@ddt
class AnnotationParserTest(unittest.TestCase):

    # Expectation data after parse
    @data((
            ("2823-3", "N", "HP:0011042"),
            ("2823-3", "H", "HP:0011042"),
            ("5803-2", "H", "HP:0032369"),
            ("2091-7", "H", "HP:0003362")
    ))
    def test_annotation_parser(self, expected_data):
        test_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 'test_annotation_file.tsv')
        annotations = AnnotationParser.parse_annotation_file(test_file)
        self.assertEqual(len(annotations), len(expected_data))
        for annotation, expected in zip(annotations, expected_data):
            self.assertEqual(annotation.loinc_id, expected[0])
            self.assertEqual(annotation.measure, expected[1])
            self.assertEqual(annotation.hpo_term, expected[2])

    @data(({"2823-3": {"N": {True: "HP:0011042"}, "H": {True: "HP:0011042"}}},
           {"5803-2": {"H": {False: "HP:0032369"}}},
           {"2091-7": {"H": {False: "HP:0003362"}}}))
    def test_annotation_parser_dict(self, expected_data):
        test_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 'test_annotation_file.tsv')
        annotations = AnnotationParser.parse_annotation_file_dict(test_file)
        for expected in expected_data:
            key = next(iter(expected))
            self.assertEqual(expected[key], annotations[key])
