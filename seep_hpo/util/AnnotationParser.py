import csv
from seep_hpo.errors.SeepParsingError import SeepParsingError
from seep_hpo.errors.SeepValidationError import SeepValidationError
from seep_hpo.models.LoincHpoAnnotation import LoincHpoAnnotation


class AnnotationParser:

    @staticmethod
    def parse_annotation_file(file_path):
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

                    annotations.append(LoincHpoAnnotation(loinc_id, loinc_scale,
                                                          measure, is_negated, hpo_term, system,
                                                          created_on,
                                                          created_by, last_edit_date,
                                                          last_edit_by,
                                                          version, finalized, comment))

                return annotations
        except (OSError, SeepParsingError, SeepValidationError) as e:
            raise e


    @staticmethod
    def parse_annotation_file_dict(file_path):
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

                    # we can make a dictionary of loincId -> List<LoincHpoAnnotation> and check
                    # if that loinc id exists and whether or not an annotation already exists.
                    # Ensures uniqueness
                    annotation = LoincHpoAnnotation(loinc_id, loinc_scale, measure, is_negated,
                                                    hpo_term,  system,  created_on,
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
                # get the list,
                annotation_list = annotations[loinc_id]
                for annotation in annotation_list:
                    if annotation.loinc_id not in remapped_annotations:
                        remapped_annotations[annotation.loinc_id] = {str(annotation.loinc_scale): {annotation.measure: {annotation.is_negated: annotation.hpo_term}}}
                    else:
                        if str(annotation.loinc_scale) not in remapped_annotations[annotation.loinc_id]:
                            remapped_annotations[annotation.loinc_id][str(annotation.loinc_scale)] = {annotation.measure: {annotation.is_negated: annotation.hpo_term}}
                        else:
                            if annotation.measure not in remapped_annotations[annotation.loinc_id][str(annotation.loinc_scale)]:
                                remapped_annotations[annotation.loinc_id][str(annotation.loinc_scale)][annotation.measure] = {annotation.is_negated: annotation.hpo_term}
                            else:
                                if is_negated not in remapped_annotations[annotation.loinc_id][str(annotation.loinc_scale)][annotation.measure]:
                                    remapped_annotations[annotation.loinc_id][str(annotation.loinc_scale)][annotation.measure][is_negated] = annotation.hpo_term
            return remapped_annotations
        except (OSError,  SeepParsingError, SeepValidationError) as e:
            raise e


