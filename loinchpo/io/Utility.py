from loinchpo.error.LoincHpoValidationError import LoincHpoValidationError


class Utility:
    """A utility class for helping to parse LoincHpoAnnotation

    This class contains static methods to validate or map fields relevant to a LoincHpoAnnotation
    file.

    """

    @staticmethod
    def is_loinc_id(loinc_id):
        """Determines whether or not the argument is a valid loinc id.

        Args:
            loinc_id: A string loinc id.

        Returns:
            Boolean if we are able to validate that string is similar to a loinc id
            (####-##)
        """
        try:
            loinc_pieces = loinc_id.split("-")
        except Exception:
            return False
        return loinc_pieces[0].isdigit() and loinc_pieces[1].isdigit()

    @staticmethod
    def is_outcome(outcome):
        """Determines whether or not the argument is a valid measure value.

        Args:
            outcome: An observed outcome for a loinc test.

        Returns:
            Boolean whether or not we accept the allowed values for provided outcome.
        """
        return outcome is not None and outcome.upper() in {"NEG", "POS", "H", "L", "N", "NEGATIVE", "POSITIVE",
                                                           "HIGH", "LOW", "NORMAL"}

    @staticmethod
    def parse_outcome(outcome):
        outcome = outcome.upper()
        if outcome == "NEG" or outcome == "NEGATIVE":
            return "NEG"
        elif outcome == "POS" or outcome == "POSITIVE":
            return "POS"
        elif outcome == "H" or outcome == "HIGH":
            return "H"
        elif outcome == "L" or outcome == "LOW":
            return "L"
        elif outcome == "N" or outcome == "NORMAL":
            return "N"

    @staticmethod
    def check_all(loinc_id, outcome):
        """Checks both loinc_id, loinc_scale, outcome for consistency.

        Based on observable negation values we return its boolean mapping.

        Args:
            loinc_id: A string loinc id
            loinc_scale: A LoincScale enumeration
            outcome: A string for the interpreted outcome for the loinc test

        Raises:
            LoincHpoValidationError: An error while validating or mapping the loinc id or observed
            measure
        """
        if not Utility.is_loinc_id(loinc_id):
            raise LoincHpoValidationError("Loinc Id {0} is not formatted properly `#-#`".
                                          format(loinc_id))
        elif not Utility.is_outcome(outcome):
            raise LoincHpoValidationError("Invalid outcome for Loinc Id {0} with value '{1}' must be "
                                          "one of [NEGATIVE, NEG], [POS, POSITIVE], [H, HIGH], [L,LOW], [N,NORMAL]."
                                          .format(loinc_id, outcome))
