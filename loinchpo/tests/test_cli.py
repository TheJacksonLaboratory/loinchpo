from click.testing import CliRunner
import unittest
import os
from loinchpo.main import cli


class CliTest(unittest.TestCase):

    def test_version_cli(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['version'])
        assert result.exit_code == 0
        assert "Version not configured yet." in result.output

    def test_resolver_cli(self):
        runner = CliRunner()
        test_annotation_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 'test_annotation_file.tsv')
        test_query_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                           'test_query.tsv')
        result = runner.invoke(cli, ['resolve', test_annotation_file, test_query_file])
        assert "HP:0011042" in result.output
        assert "HP:0003362" in result.output
