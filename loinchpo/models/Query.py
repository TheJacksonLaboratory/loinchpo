from loinchpo.util.AnnotationUtility import AnnotationUtility
from loinchpo.errors.SeepValidationError import SeepValidationError


class Query:
    def __init__(self, loinc_id, measure, negated):
        try:
            AnnotationUtility.check_all(loinc_id, measure)
            self.loinc_id = loinc_id
            self.measure = measure
            self.negated = AnnotationUtility.interpret_negated(self.loinc_id, negated)
        except SeepValidationError as e:
            raise e
