from seep_hpo.errors.SeepValidationError import SeepValidationError


class AnnotationSanity:

    @staticmethod
    def is_loinc_id(loinc_id):
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
        if measure and measure.upper() in ["NEG", "POS", "H", "L", "N"]:
            return True
        return False

    @staticmethod
    def is_negated(negated):
        return negated in [True, False]

    @staticmethod
    def check_all(loinc_id, measure):
        if not AnnotationSanity.is_loinc_id(loinc_id):
            raise SeepValidationError("Loinc Id {0} is not formatted properly `#-#`".
                                      format(loinc_id))
        elif not AnnotationSanity.is_measure(measure):
            raise SeepValidationError("Invalid measure for Loinc Id {0} with value '{1}' must be "
                                      "one of NEG, POS, H, L". format(loinc_id, measure))

