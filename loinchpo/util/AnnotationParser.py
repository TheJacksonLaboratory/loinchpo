import csv
from loinchpo.errors.LoincHpoParsingError import LoincHpoParsingError
from loinchpo.errors.LoincHpoValidationError import LoincHpoValidationError
from loinchpo.util.AnnotationUtility import AnnotationUtility
from loinchpo.models.LoincScale import LoincScale
from collections import namedtuple

LoincHpoAnnotation = namedtuple('LoincHpoAnnotation',
                                'loinc_id, loinc_scale, outcome, hpo_term,'
                                'supplemental_term, curators, comment')


class AnnotationParser:
    """ Provides methods for parsing Loinc2HpoAnnotation files.

        Typical usage example:

        annotations = AnnotationParser.parse_annotation_file(file_path)
        annotation_map = AnnotationParser.parse_annotation_file_dict(file_path)

    """

    @staticmethod
    def parse_annotation_file(file_path):
        """ Parsing Loinc2HpoAnnotation files to a list of namedtuples LoincHpoAnnotation.

        Args:
            file_path: A string file path to the annotation file.

        Returns:
            A list of namedtuples 'LoincHpoAnnotation'.

            [LoincHpoAnnotation, LoincHpoAnnotation]

        Raises:
            OSError: When the file could not be opened or found.
            LoincHpoParsingError: When there were issues with file format
            LoincHpoValidationError: When there were issues with specific field expected values.
        """
        annotations = []

        try:
            with open(file_path) as f:
                reader = csv.reader(f, delimiter='\t')
                # Skip first line
                fields = next(reader)
                # Throw exception if it doesnt look like header line.
                if "loincId" not in fields:
                    raise LoincHpoParsingError("Header Line not Loinc2Hpo annotation file.")
                for line in reader:
                    loinc_id, loinc_scale, outcome, hpo_term, supplemental_term, curators, comment = line

                    # Sanity Check loinc_id and other things like in the class.
                    AnnotationUtility.check_all(loinc_id, outcome)

                    # Map the Loinc Scale
                    loinc_scale = LoincScale.parse(loinc_scale)

                    # Build named tuple if we are okay. Append to list.
                    annotations.append(LoincHpoAnnotation(loinc_id, loinc_scale, outcome,
                                                          hpo_term, supplemental_term, curators, comment))
                return annotations
        except (OSError, LoincHpoParsingError, LoincHpoValidationError) as e:
            raise e

    @staticmethod
    def parse_annotation_file_dict(file_path):
        """ Parsing Loinc2HpoAnnotation files to a traversable dictionary

            This method has a specific return of a dictionary of dictionaries to help us query or
            traverseannotations when resolving input queries from users.

        Args:
            file_path: A string file path to the annotation file.

        Returns:
            A dictionary of dictionaries with a specific mapping to help us query for
            loinc code, measures and negations to get us an hpo code.

            {'29298-0': {'POS': 'HP:0009281'}}

            In this example we see that a loinc_id has a measure of positive and it is not negated
            which results in an hpo code.

        Raises:
            OSError: When the file could not be opened or found.
            LoincHpoParsingError: When there were issues with file format
            LoincHpoValidationError: When there were issues with specific field expected values.
        """
        annotations = {}
        try:
            with open(file_path) as f:
                reader = csv.reader(f, delimiter='\t')
                fields = next(reader)
                if "loincId" not in fields:
                    raise LoincHpoParsingError("Header Line not Loinc2Hpo annotation file.")
                for line in reader:
                    loinc_id, loinc_scale, outcome, hpo_term, supplemental_term, curators, comment = line

                    # Sanity Check loinc_id and other things like in the class.
                    AnnotationUtility.check_all(loinc_id, outcome)

                    # Map the Loinc Scale
                    loinc_scale = LoincScale.parse(loinc_scale)

                    # Build named tuple if we are okay. Append to list.
                    annotation = LoincHpoAnnotation(loinc_id, loinc_scale, outcome, hpo_term, supplemental_term,
                                                    curators, comment)
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
    def parse_annotation_pandas_dict(df):
        """ Parsing Loinc2HpoAnnotation pandas to a traversable dictionary

            This method has a specific return of a dictionary of dictionaries to help us query or
            traverseannotations when resolving input queries from users.

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
            SeepParsingError: When there were issues with file format
            SeepValidationError: When there were issues with specific field expected values.
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

                # Map the loinc scale
                loinc_scale = LoincScale.parse(loinc_scale)

                # Sanity Check loinc_id and other things like in the class.
                AnnotationUtility.check_all(loinc_id, outcome)

                # Build named tuple if we are okay. Append to list.
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