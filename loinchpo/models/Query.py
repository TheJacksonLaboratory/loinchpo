from loinchpo.util.AnnotationUtility import AnnotationUtility
from loinchpo.errors.LoincHpoValidationError import LoincHpoValidationError


class Query:
    def __init__(self, loinc_id, measure, negated):
        try:
            AnnotationUtility.check_all(loinc_id, measure)
            self.loinc_id = loinc_id
            self.measure = measure.upper()
            self.negated = AnnotationUtility.interpret_negated(self.loinc_id, negated)
        except LoincHpoValidationError as e:
            raise e
