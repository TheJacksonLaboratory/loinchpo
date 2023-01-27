from loinchpo.error.LoincHpoParsingError import LoincHpoParsingError


class LoincId:
    """
        A class to represent a loinc id

    """
    def __init__(self, loinc_id):
        self.num, self.suffix, self.loinc_id = self._parse_loinc_id(loinc_id)

    @staticmethod
    def _parse_loinc_id(loinc_id):
        try:
            num, suffix = loinc_id.split("-")
            return num, suffix, loinc_id
        except (ValueError, AttributeError):
            raise LoincHpoParsingError("Malformed Loinc code {0}".format(loinc_id))
