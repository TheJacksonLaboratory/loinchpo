import csv
from loinchpo.errors.SeepParsingError import SeepParsingError
from loinchpo.errors.SeepValidationError import SeepValidationError
from loinchpo.util.AnnotationUtility import AnnotationUtility
from loinchpo.models.LoincScale import LoincScale
from collections import namedtuple

LoincHpoAnnotation = namedtuple('LoincHpoAnnotation',
                                'loinc_id, loinc_scale, system, measure, hpo_term, '
                                'is_negated, created_on, created_by, last_edit_date, '
                                'last_edit_by, version, finalized, comment')


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
            SeepParsingError: When there were issues with file format
            SeepValidationError: When there were issues with specific field expected values.
        """
        annotations = []

        try:
            with open(file_path) as f:
                reader = csv.reader(f, delimiter='\t')
                # Skip first line
                fields = next(reader)
                # Throw exception if it doesnt look like header line.
                if "loincId" not in fields:
                    raise SeepParsingError("Header Line not Loinc2Hpo annotation file.")
                for line in reader:
                    loinc_id, loinc_scale, system, measure, hpo_term, is_negated, created_on, \
                        created_by, last_edit_date, last_edit_by, version, finalized, comment = line

                    # Sanity Check loinc_id and other things like in the class.
                    AnnotationUtility.check_all(loinc_id, measure)
                    # Parse Negation
                    is_negated = AnnotationUtility.interpret_negated(loinc_id, is_negated)
                    # Map the Loinc Scale
                    loinc_scale = LoincScale.map_loinc_scale(loinc_scale)

                    # Build named tuple if we are okay. Append to list.
                    annotations.append(LoincHpoAnnotation(loinc_id, loinc_scale, system, measure,
                                                          hpo_term, is_negated, created_on,
                                                          created_by, last_edit_date, last_edit_by,
                                                          version, finalized, comment))
                return annotations
        except (OSError, SeepParsingError, SeepValidationError) as e:
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

            {'29298-0': {'POS': {'N': 'HP:0009281'}}}

            In this example we see that a loinc_id has a measure of positive and it is not negated
            which results in an hpo code.

        Raises:
            OSError: When the file could not be opened or found.
            SeepParsingError: When there were issues with file format
            SeepValidationError: When there were issues with specific field expected values.
        """
        annotations = {}
        try:
            with open(file_path) as f:
                reader = csv.reader(f, delimiter='\t')
                fields = next(reader)
                if "loincId" not in fields:
                    raise SeepParsingError("Header Line not Loinc2Hpo annotation file.")
                for line in reader:
                    loinc_id, loinc_scale, system, measure, hpo_term, is_negated, created_on, \
                    created_by, last_edit_date, last_edit_by, version, finalized, comment = line

                    # Sanity Check loinc_id and other things like in the class.
                    AnnotationUtility.check_all(loinc_id, measure)
                    # Parse Negation
                    is_negated = AnnotationUtility.interpret_negated(loinc_id, is_negated)
                    # Map the Loinc Scale
                    loinc_scale = LoincScale.map_loinc_scale(loinc_scale)

                    # Build named tuple if we are okay. Append to list.
                    annotation = LoincHpoAnnotation(loinc_id, loinc_scale, system, measure,
                                                    hpo_term, is_negated, created_on,
                                                    created_by, last_edit_date, last_edit_by,
                                                    version, finalized, comment)
                    if loinc_id in annotations:
                        if annotation in annotations[loinc_id]:
                            raise SeepParsingError("Duplicate annotation exists for loinc code.")
                        else:
                            annotations[loinc_id].append(annotation)
                    else:
                        annotations[loinc_id] = [annotation]
            # remapping to a queryable dictionary given specific outcomes.
            # loinc_id -> scale -> measure -> negated -> term
            remapped_annotations = {}
            for loinc_id in annotations:
                # get the list
                annotation_list = annotations[loinc_id]
                for annotation in annotation_list:
                    if annotation.loinc_id not in remapped_annotations:
                        remapped_annotations[annotation.loinc_id] = {annotation.measure: {annotation.is_negated: annotation.hpo_term}}
                    else:
                        if annotation.measure not in remapped_annotations[annotation.loinc_id]:
                            remapped_annotations[annotation.loinc_id][annotation.measure] = \
                                {annotation.is_negated: annotation.hpo_term}
                        else:
                            if is_negated not in \
                                    remapped_annotations[annotation.loinc_id][annotation.measure]:
                                remapped_annotations[annotation.loinc_id][annotation.measure][is_negated] = annotation.hpo_term
            return remapped_annotations
        except (OSError,  SeepParsingError, SeepValidationError) as e:
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
        expected_fields = ("loincId", "loincScale",	"system", "code", "hpoTermId", "isNegated", "createdOn", 
        "createdBy", "lastEditedOn", "lastEditedBy", "version", "isFinalized", "comment")
        try:
            cols = df.columns
            if not all(col in expected_fields for col in cols):
                raise SeepParsingError("Dataframe columns not correct, must be (loincId	loincScale	system	code " + 
                    "hpoTermId	isNegated	createdOn	createdBy	lastEditedOn	lastEditedBy	version	isFinalized	comment)")
            for row in df.iterrows():
                loinc_id, loinc_scale, system, measure, hpo_term, is_negated, created_on, \
                created_by, last_edit_date, last_edit_by, version, finalized, comment = row[1].tolist()

                # Sanity Check loinc_id and other things like in the class.
                AnnotationUtility.check_all(loinc_id, measure)
                # Parse Negation
                is_negated = AnnotationUtility.interpret_negated(loinc_id, is_negated)
                # Map the Loinc Scale
                loinc_scale = LoincScale.map_loinc_scale(loinc_scale)

                # Build named tuple if we are okay. Append to list.
                annotation = LoincHpoAnnotation(loinc_id, loinc_scale, system, measure,
                                                hpo_term, is_negated, created_on,
                                                created_by, last_edit_date, last_edit_by,
                                                version, finalized, comment)
                if loinc_id in annotations:
                    if annotation in annotations[loinc_id]:
                        raise SeepParsingError("Duplicate annotation exists for loinc code.")
                    else:
                        annotations[loinc_id].append(annotation)
                else:
                    annotations[loinc_id] = [annotation]
            # remapping to a queryable dictionary given specific outcomes.
            # loinc_id -> scale -> measure -> negated -> term
            remapped_annotations = {}
            for loinc_id in annotations:
                # get the list
                annotation_list = annotations[loinc_id]
                for annotation in annotation_list:
                    if annotation.loinc_id not in remapped_annotations:
                        remapped_annotations[annotation.loinc_id] = {annotation.measure: {annotation.is_negated: annotation.hpo_term}}
                    else:
                        if annotation.measure not in remapped_annotations[annotation.loinc_id]:
                            remapped_annotations[annotation.loinc_id][annotation.measure] = \
                                {annotation.is_negated: annotation.hpo_term}
                        else:
                            if is_negated not in \
                                    remapped_annotations[annotation.loinc_id][annotation.measure]:
                                remapped_annotations[annotation.loinc_id][annotation.measure][is_negated] = annotation.hpo_term
            return remapped_annotations
        except (OSError,  SeepParsingError, SeepValidationError) as e:
            raise e


