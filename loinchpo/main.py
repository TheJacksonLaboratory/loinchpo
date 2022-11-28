import sys
import click
from loinchpo import AnnotationParser
from loinchpo import QueryResolver
from loinchpo import QueryFileParser

@click.group()
def cli():
    pass


@cli.command()
@click.argument('annotation_path', type=click.Path(exists=True))
@click.argument('query_path', type=click.Path(exists=True))
def resolve(annotation_path, query_path):
    """Command to resolve queries to hpo codes
    Todo:
        * Need to make this better reporting to a file
    Args:
        annotation_path (str): is the path to the LOINC HPO Annotation File.
        query_path (str): is the path to your file with Loinc Id's, Measures, Negations.
    """
    click.echo("Parsing annotation files...")
    click.echo(click.format_filename(annotation_path))
    click.echo(click.format_filename(query_path))
    annotations = AnnotationParser.parse_annotation_file(annotation_path)
    queries = QueryFileParser.parse(query_path)
    resolver = QueryResolver(annotations)
    click.echo("Resolving your queries...")
    for query in queries:
        result = resolver.resolve(query)
        print(result)
    click.echo("Done.")


@cli.command()
def version():
    """Command to check the version of LOINC2HPO"""
    click.echo("Version not configured yet.")


if __name__ == '__main__':
    sys.exit(cli())
