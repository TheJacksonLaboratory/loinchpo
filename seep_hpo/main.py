import sys
import click
from seep_hpo.util.AnnotationParser import AnnotationParser
from seep_hpo.util.AnnotationResolver import AnnotationResolver

@click.group()
def cli():
    pass


@cli.command()
@click.argument('filename', type=click.Path(exists=True))
@click.argument('')
def resolve(filename):
    """Command to resolve loinc 2 hpo mappings.

    FILENAME is the path to the LOINC HPO Annotation File.
    """
    click.echo(click.format_filename(filename))
    click.echo("Parsing annotation file...")
    annotations = AnnotationParser.parse_annotation_file_dict(filename)
    click.echo(len(annotations))


@cli.command()
def version():
    """Command to check the version of LOINC2HPO"""
    click.echo("Version not configured yet.")


if __name__ == '__main__':
    sys.exit(cli())
