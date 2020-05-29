from seep_hpo.models.LoincScale import LoincScale
from seep_hpo.util.AnnotationSanity import AnnotationSanity
from seep_hpo.errors.SeepValidationError import SeepValidationError


class LoincHpoAnnotation:
    def __init__(self, loinc_id, measure, is_negated, hpo_term, loinc_scale, system, created_on,
                 created_by, last_edit_date, last_edit_by, version, finalized, comment):
        try:
            AnnotationSanity.check_all(loinc_id, measure)
            self.loinc_id = loinc_id
            self.loinc_scale = LoincScale.map_loinc_scale(loinc_scale)
            self.system = system
            self.measure = measure
            self.hpo_term = hpo_term
            self.is_negated = AnnotationSanity.interpret_negated(self.loinc_id, is_negated)
            self.created_on = created_on
            self.created_by = created_by
            self.last_edit_date = last_edit_date
            self.last_edit_by = last_edit_by
            self.version = version
            self.finalized = finalized
            self.comment = comment
        except SeepValidationError as e:
            raise e

    def __eq__(self, o: object) -> bool:
        return super().__eq__(o)






