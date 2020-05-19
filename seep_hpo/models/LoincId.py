from seep_hpo.errors.LoincParsingError import LoincParsingError


class LoincId:
    def __init__(self, loinc_id):
        try:
            self.num, self.suffix, self.loinc_id = self.parse_loinc_id(loinc_id)
        except LoincParsingError:
            raise

    def parse_loinc_id(self, loinc_id):
        try:
            num, suffix = loinc_id.split("-")
            return num, suffix, loinc_id
        except (ValueError, AttributeError):
            raise LoincParsingError("Malformed Loinc code {0}".format(loinc_id))