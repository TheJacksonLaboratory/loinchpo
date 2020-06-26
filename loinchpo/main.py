import sys
import click
from loinchpo.util.AnnotationParser import AnnotationParser
from loinchpo.util.AnnotationResolver import AnnotationResolver
from loinchpo.util.QueryFileParser import QueryFileParser

@click.group()
def cli():
    pass


@cli.command()
@click.argument('annotation_path', type=click.Path(exists=True))
@click.argument('query_path', type=click.Path(exists=True))
def resolve(annotation_path, query_path):
    """Command to resolve queries to hpo codes

    ANNOTATION_PATH is the path to the LOINC HPO Annotation File.
    QUERY_PATH is the path to your file with Loinc Id's, Measures, Negations.
    """
    click.echo("Parsing annotation files...")
    click.echo(click.format_filename(annotation_path))
    click.echo(click.format_filename(query_path))
    annotations = AnnotationParser.parse_annotation_file_dict(annotation_path)
    queries = QueryFileParser.parse(query_path)
    resolver = AnnotationResolver(annotations)
    click.echo("Resolving your queries...")
    for query in queries:
        result = resolver.resolve(query)
        print(result)
    click.echo("Done.")
    # Then we need to read in the queries. For each query we will call the resolver.
    # Then write a reporter to report our findings in different formats.


@cli.command()
def version():
    """Command to check the version of LOINC2HPO"""
    click.echo("Version not configured yet.")


if __name__ == '__main__':
    sys.exit(cli())
