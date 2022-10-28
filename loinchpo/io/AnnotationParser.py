import csv
from loinchpo.error.LoincHpoParsingError import LoincHpoParsingError
from loinchpo.error.LoincHpoFileValidationError import LoincHpoValidationError
from loinchpo.io.Utility import Utility
from loinchpo.model.LoincScale import LoincScale
from collections import namedtuple

LoincHpoAnnotation = namedtuple('LoincHpoAnnotation',
                                'loinc_id, loinc_scale, outcome, hpo_term,'
                                'supplemental_term, curators, comment')


class AnnotationParser:
    """ Provides methods for parsing :class:`LoincHpoAnnotation` files.

        Example:
            annotations = AnnotationParser.parse_annotation_file(file_path)
            annotation_map = AnnotationParser.parse_annotation_file_dict(file_path)

    """

    @staticmethod
    def parse_annotation_file(file_path, ls=False):
        """ A traversable dictionary of loinc_id -> loinc_measure -> negation Parsing Loinc2HpoAnnotation files to
        either a list of namedtuples :class:`LoincHpoAnnotation`

        Args:
            file_path: A string file path to the annotation file.
            ls: Should the method return a list of ::class::`LoincHpoAnnotation`

        Returns:
            annotations: A dictionary of loinc_id -> loinc_measure -> negation or a list of namedtuples ::class::`LoincHpoAnnotation`

        Raises:
            OSError: When the file could not be opened or found.
            LoincHpoParsingError: When there were issues with file format
            LoincHpoValidationError: When there were issues with specific field expected values.
        """

        annotations = {}
        if ls:
            annotations = []
        try:
            with open(file_path) as f:
                reader = csv.reader(f, delimiter='\t')
                fields = next(reader)

                if "loincId" not in fields:
                    raise LoincHpoParsingError("Header Line not Loinc2Hpo annotation file.")
                for line in reader:
                    loinc_id, loinc_scale, outcome, hpo_term, supplemental_term, curators, comment = line

                    Utility.check_all(loinc_id, outcome)
                    loinc_scale = LoincScale.parse(loinc_scale)
                    outcome = Utility.parse_outcome(outcome)

                    annotation = LoincHpoAnnotation(loinc_id, loinc_scale, outcome, hpo_term, supplemental_term,
                                                    curators, comment)

                    if not ls:
                        if loinc_id in annotations:
                            if annotation in annotations[loinc_id]:
                                raise LoincHpoParsingError("Duplicate annotation exists for loinc code.")
                            else:
                                annotations[loinc_id].append(annotation)
                        else:
                            annotations[loinc_id] = [annotation]
                    else:
                        annotations.append(annotation)

                if not ls:
                    return AnnotationParser._build_query_map(annotations)
                else:
                    return annotations
        except (OSError, LoincHpoParsingError, LoincHpoValidationError) as e:
            raise e

    @staticmethod
    def parse_annotation(df):
        """ Parsing pandas dataframe to a traversable dictionary

            This method has a specific return of a dictionary of dictionaries to help us query or
            traverse annotations when resolving input queries from users.

        Args:
            df: A pandas dataframe with loinc queries. (loincId, loincMeasure, negated)

        Returns:
            A dictionary of dictionaries with a specific mapping to help us query for
            loinc code, measures and negations to get us an hpo code.

            {'29298-0': {'POS': {'N': 'HP:0009281'}}}

            In this example we see that a loinc_id has a measure of positive and it is not negated
            which results in an hpo code.

        Raises:
            OSError: When the file could not be opened or found.
            LoincHpoParsingError: When there were issues with file format
            LoincHpoValidationError: When there were issues with specific field expected values.
        """
        annotations = {}
        expected_fields = ("loincId", "loincScale", "outcome", "hpoTermId", "supplementalTermId", "curation", "comment")
        try:
            cols = df.columns
            if not all(col in expected_fields for col in cols):
                raise LoincHpoParsingError(
                    "Dataframe columns not correct, must be (loincId, loincScale,  outcome, " +
                    "hpoTermId,	supplmentalTermId, curator, comment)")
            for row in df.iterrows():
                loinc_id, loinc_scale, outcome, hpo_term, supplemental_term, curators, comment = row[1].tolist()

                loinc_scale = LoincScale.parse(loinc_scale)
                Utility.check_all(loinc_id, outcome)
                outcome = Utility.parse_outcome(outcome)

                annotation = LoincHpoAnnotation(loinc_id, loinc_scale, outcome, hpo_term, supplemental_term, curators,
                                                comment)
                if loinc_id in annotations:
                    if annotation in annotations[loinc_id]:
                        raise LoincHpoParsingError("Duplicate annotation exists for loinc code.")
                    else:
                        annotations[loinc_id].append(annotation)
                else:
                    annotations[loinc_id] = [annotation]

            return AnnotationParser._build_query_map(annotations)
        except (OSError, LoincHpoParsingError, LoincHpoValidationError) as e:
            raise e

    @staticmethod
    def _build_query_map(annotations):
        """
            remapping to a queryable dictionary given specific outcomes.
            loinc_id -> scale -> outcome -> negated -> term
        """
        query_map = {}
        for loinc_id in annotations:
            # get the list
            annotation_list = annotations[loinc_id]
            for annotation in annotation_list:
                if annotation.loinc_id not in query_map:
                    query_map[annotation.loinc_id] = {annotation.outcome: annotation.hpo_term}
                else:
                    if annotation.outcome not in query_map[annotation.loinc_id]:
                        query_map[annotation.loinc_id][annotation.outcome] = annotation.hpo_term
        return query_map
