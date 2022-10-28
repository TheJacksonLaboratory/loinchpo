from enum import Enum, auto


class LoincScale(Enum):
    """ An enumeration representation for the possible loinc scale types.

    """
    QN = 1, "qn"
    ORD = 2, "ord"
    ORDQN = 3, "ordqn"
    NOM = 4, "nom"
    NAR = 5, "nar"
    MULTI = 6, "multi"
    DOC = 7, "doc"
    SET = 8, "set"
    UNKNOWN = auto()

    @staticmethod
    def parse(loinc_scale):
        """Mapping loinc scale to enumeration.

        Args:
            loinc_scale: A parsed string loinc scale from LoincHpoAnnotation file.

        Returns:
            An enumeration representation of loinc_scale or enumeration unknown for those that
            could not be mapped to an associated enumeration.
        """
        try:
            return LoincScale[loinc_scale.upper()]
        except (KeyError, AttributeError):
            return LoincScale.UNKNOWN

    @staticmethod
    def infer_long(long_name: str):
        """
            Helper function to infer long_name from a list of synonyms
        """

        if "quantitative" in long_name and "ordinal" in long_name:
            return str(LoincScale.ORDQN)
        elif "ordinal" in long_name:
            return str(LoincScale.ORD)
        elif "quantitative" in long_name:
            return str(LoincScale.QN)
        elif "nominal" in long_name or "qualitative" in long_name:
            return str(LoincScale.NOM)
        elif "narrative" in long_name:
            return str(LoincScale.NAR)
        elif "doc" in long_name:
            return str(LoincScale.DOC)
        elif "set" in long_name:
            return str(LoincScale.SET)
        elif "multi" in long_name:
            return str(LoincScale.MULTI)
        elif "panel" in long_name or "pnl" in long_name or "panl" in long_name:
            return str(LoincScale.SET)
        return str(LoincScale.UNKNOWN)

    def __str__(self):
        if self == LoincScale.QN:
            return "QN"
        elif self == LoincScale.ORD:
            return "ORD"
        elif self == LoincScale.ORDQN:
            return "ORDQN"
        elif self == LoincScale.NOM:
            return "NOM"
        elif self == LoincScale.NAR:
            return "NAR"
        elif self == LoincScale.MULTI:
            return "MULTI"
        elif self == LoincScale.DOC:
            return "DOC"
        elif self == LoincScale.SET:
            return "SET"
        else:
            return "UNKNOWN"
