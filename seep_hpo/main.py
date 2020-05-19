import sys
import click


@click.group()
def cli():
    pass


@cli.command()
def version():
    """Command to check the version of LOINC2HPO"""
    click.echo("Version not configured yet.")


if __name__ == '__main__':
    sys.exit(cli())
