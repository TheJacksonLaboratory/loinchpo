from loinchpo.io.Utility import Utility
from loinchpo.error.LoincHpoValidationError import LoincHpoValidationError


class Query:
    def __init__(self, loinc_id, outcome):
        try:
            Utility.check_all(loinc_id, outcome)
            self.loinc_id = loinc_id
            self.outcome = Utility.parse_outcome(outcome.upper())
        except LoincHpoValidationError as e:
            raise e
