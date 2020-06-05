from enum import Enum, auto


class LoincScale(Enum):
    """ An enumeration representation for the possible loinc scale types.

    """
    QN = 1, "qn"
    ORD =  2, "ord"
    ORDQN = 3, "ordqn",
    NOM = 4, "nom",
    NAR = 5, "nar",
    MULTI = 6, "multi",
    DOC = 7, "doc",
    SET = 8, "set",
    UNKNOWN = auto()

    @staticmethod
    def map_loinc_scale(loinc_scale):
        """Mapping loinc scale to enumeration.

        Args:
            loinc_scale: A parsed string loinc scale from LoincHpoAnnotation file.

        Returns:
            An enumeration representation of loinc_scale or enumeration unknown for those that
            could not be mapped to an associated enumeration.
        """
        try:
            return LoincScale[loinc_scale.upper()]
        except (KeyError, AttributeError) as e:
            return LoincScale.UNKNOWN

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
            return "set"
        else:
            return "unknown"
