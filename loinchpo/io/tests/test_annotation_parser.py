import unittest
import os
from ddt import ddt, data
import pandas as pd
from loinchpo import AnnotationParser


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
        annotations = AnnotationParser.parse_annotation_file(test_file, ls=True)
        self.assertEqual(len(annotations), len(expected_data))
        for annotation, expected in zip(annotations, expected_data):
            self.assertEqual(annotation.loinc_id, expected[0])
            self.assertEqual(annotation.outcome, expected[1])
            self.assertEqual(annotation.hpo_term, expected[2])

    @data(({"2823-3": {"N": "HP:0011042", "H": "HP:0011042"}},
           {"5803-2": {"H": "HP:0032369"}},
           {"2091-7": {"H": "HP:0003362"}}))
    def test_annotation_parser_file(self, expected_data):
        test_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 'test_annotation_file.tsv')
        annotations = AnnotationParser.parse_annotation_file(test_file)
        for expected in expected_data:
            key = next(iter(expected))
            self.assertEqual(expected[key], annotations[key])

    @data(
        ({
         "loincId": ["2823-3", "2823-3", "5803-2", "2091-7"],
         "loincScale": ["Qn","Qn","Qn","Qn"],
         "outcome": ["N", "H", "H", "H"],
         "hpoTermId": ["HP:0011042", "HP:0011042", "HP:0032369", "HP:0003362"],
         "supplementalTermId": [".", ".", ".", "."],
         "curation": ["A", "B", "C", "D"],
         "comment": ["", "", "", ""]
        })
    )
    def test_annotation(self, input_frame):
        expected_data = ({"2823-3": {"N": "HP:0011042", "H": "HP:0011042"}},
           {"5803-2": {"H": "HP:0032369"}},
           {"2091-7": {"H": "HP:0003362"}})
        frame = pd.DataFrame(input_frame, columns=['loincId', 'loincScale',
        'outcome', 'hpoTermId', 'supplementalTermId', 'curation', 'comment'])
        annotations = AnnotationParser.parse_annotation(frame)
        for expected in expected_data:
            key = next(iter(expected))
            self.assertEqual(expected[key], annotations[key])