from loinchpo.util.AnnotationUtility import AnnotationUtility
from loinchpo.errors.LoincHpoValidationError import LoincHpoValidationError


class Query:
    def __init__(self, loinc_id, outcome):
        try:
            AnnotationUtility.check_all(loinc_id, outcome)
            self.loinc_id = loinc_id
            self.outcome = outcome.upper()
        except LoincHpoValidationError as e:
            raise e
