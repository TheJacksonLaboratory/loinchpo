from loinchpo.errors.SeepValidationError import SeepValidationError


class AnnotationResolver:
    """ Resolve annotation queries to hpo codes

        Example:
            annotations = AnnotationParser.parse_annotation_file_dict(file_path)
            resolver = AnnotationResolver(annotations)
            query = Query(loinc_id, measure, negated)
            single_hpo_code = resolver.resolve(query)


        Attributes:
            annotations: A dictionary of dictionaries from AnnotationParser.

    """
    def __init__(self, annotations):
        self.annotations = annotations

    def resolve(self, query):
        """ Resolving a single query to a hpo code

        Args:
            query: An instance of Query, which contains the query with proper values.

        Returns:
            A single string hpo code or empty string if no annotation found.
        """
        try:
            # Transform inputs into expectations
            return self.annotations[query.loinc_id][query.measure][query.negated]
        except (KeyError, SeepValidationError):
            return ""
