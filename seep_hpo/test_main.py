from click.testing import CliRunner
import unittest
from . import main


class CliTest(unittest.TestCase):

    def test_version_cli(self):
        runner = CliRunner()
        result = runner.invoke(main.cli, ['version'])
        assert result.exit_code == 0
        assert "Version not configured yet." in result.output
