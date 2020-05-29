from seep_hpo.util.AnnotationSanity import AnnotationSanity
from seep_hpo.errors.SeepValidationError import SeepValidationError


class Query:
    def __init__(self, loinc_id, measure, negated):
        try:
            AnnotationSanity.check_all(loinc_id, measure)
            self.loinc_id = loinc_id
            self.measure = measure
            self.negated = AnnotationSanity.interpret_negated(self.loinc_id, negated)
        except SeepValidationError as e:
            raise e
