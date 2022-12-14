from loinchpo import Utility
from loinchpo.error.LoincHpoFileValidationError import LoincHpoValidationError


class Query:
    def __init__(self, loinc_id, outcome):
        try:
            Utility.check_all(loinc_id, outcome)
            self.loinc_id = loinc_id
            self.outcome = Utility.parse_outcome(outcome)
        except LoincHpoValidationError as e:
            raise e
