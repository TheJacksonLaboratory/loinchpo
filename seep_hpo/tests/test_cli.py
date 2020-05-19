from click.testing import CliRunner
import unittest
from ..main import cli


class CliTest(unittest.TestCase):

    def test_version_cli(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['version'])
        assert result.exit_code == 0
        assert "Version not configured yet." in result.output
