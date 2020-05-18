#import logging
import sys
import click
#DEFAULT_LOG_FMT = '%(asctime)s %(name)-20s %(levelname)-3s : %(message)s'
#logging.basicConfig(level=logging.INFO, format=DEFAULT_LOG_FMT)
#logger = logging.getLogger('seep_hpo')
#logger.info("Fake Version Here")


@click.group()
def cli():
    pass


@cli.command()
def version():
    """Command to check the version of LOINC2HPO"""
    click.echo("Version not configured yet.")


if __name__ == '__main__':
    sys.exit(cli())
