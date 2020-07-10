from loinchpo.errors.SeepValidationError import SeepValidationError


class AnnotationUtility:
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
            # if we can split by dash and parse into numbers
            # we assume its a loinc structure.
            loinc_pieces = loinc_id.split("-")
            if int(loinc_pieces[0]) and int(loinc_pieces[1]):
                return True
        except Exception:
            return False

    @staticmethod
    def is_measure(measure):
        """Determines whether or not the argument is a valid measure value.

        Args:
            measure: An observed measure for a loinc code.

        Returns:
            Boolean whether or not we accept the allowed values for measures.
        """
        if measure and measure.upper() in {"NEG", "POS", "H", "L", "N"}:
            return True
        return False

    @staticmethod
    def is_negated(negated):
        return negated in {True, False}

    @staticmethod
    def interpret_negated(loinc_id, negated):
        """Parses negation value to python boolean.

        Based on observable negation values we return its boolean mapping.

        Args:
            loinc_id: A string loinc id for the associated negation.
            negated: A boolean for whether or not this loinc_id is negated.

        Returns:
            Boolean whether or not we accept the allowed values for measures.

        Raises:
            SeepValidationError: An error while validating or mapping the input to a boolean.
        """
        negated = str(negated).upper()
        try:
            mapping = {"TRUE": True, "1": True, "YES": True,
                       "FALSE": False, "0": False, "NO": False
                       }
            return mapping[negated]
        except KeyError:
            raise SeepValidationError("Invalid Negated value for Loinc Id {0} value {1}".
                                      format(loinc_id, negated))

    @staticmethod
    def check_all(loinc_id, measure):
        """Checks both loinc_id and measure for consistency.

        Based on observable negation values we return its boolean mapping.

        Args:
            loinc_id: A string loinc id
            measure: A string for the observed measure

        Raises:
            SeepValidationError: An error while validating or mapping the loinc id or observed
            measure
        """
        if not AnnotationUtility.is_loinc_id(loinc_id):
            raise SeepValidationError("Loinc Id {0} is not formatted properly `#-#`".
                                      format(loinc_id))
        elif not AnnotationUtility.is_measure(measure):
            raise SeepValidationError("Invalid measure for Loinc Id {0} with value '{1}' must be "
                                      "one of NEG, POS, H, L". format(loinc_id, measure))

