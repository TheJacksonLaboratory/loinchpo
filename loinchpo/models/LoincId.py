from loinchpo.errors.LoincHpoParsingError import LoincHpoParsingError


class LoincId:
    def __init__(self, loinc_id):
        self.num, self.suffix, self.loinc_id = self.parse_loinc_id(loinc_id)

    def parse_loinc_id(self, loinc_id):
        try:
            num, suffix = loinc_id.split("-")
            return num, suffix, loinc_id
        except (ValueError, AttributeError):
            raise LoincHpoParsingError("Malformed Loinc code {0}".format(loinc_id))