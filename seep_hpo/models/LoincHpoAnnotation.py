from seep_hpo.models.LoincScale import LoincScale
from seep_hpo.util.AnnotationSanity import AnnotationSanity
from seep_hpo.errors.SeepValidationError import SeepValidationError


class LoincHpoAnnotation:
    def __init__(self, loinc_id, loinc_scale, measure, is_negated, hpo_term=None, system=None, created_on=None,
                 created_by=None, last_edit_date=None, last_edit_by=None, version=None, finalized=None, comment=None):
        try:
            AnnotationSanity.check_all(loinc_id, measure)
            self.loinc_id = loinc_id
            self.loinc_scale = LoincScale.map_loinc_scale(loinc_scale)
            self.system = system
            self.measure = measure
            self.hpo_term = hpo_term
            self.is_negated = self._interpret_negated(is_negated)
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

    def _interpret_negated(self, negated):
        negated = str(negated).upper()
        try:
            mapping = {"TRUE": True, "1": True, "YES": True,
                       "FALSE": False, "0": False, "NO": False
                       }
            return mapping[negated]
        except KeyError:
            raise SeepValidationError("Invalid Negated value for Loinc Id {0} value {1}".
                                      format(self.loinc_id, negated))






