from seep_hpo.errors.SeepValidationError import SeepValidationError
from seep_hpo.errors.SeepResolvingError import SeepResolvingError
from seep_hpo.models.LoincHpoAnnotation import LoincHpoAnnotation


class AnnotationResolver:
    def __init__(self, annotations):
        self.annotations = annotations

    def resolve(self, loinc_id, loinc_scale, measure, negated):
        try:
            # Transform inputs into expectations
            annotation = LoincHpoAnnotation(loinc_id, loinc_scale, measure, negated)
            return self.annotations[annotation.loinc_id][str(annotation.loinc_scale)][annotation.measure][annotation.is_negated]
        except (KeyError, SeepValidationError) as e:
            if e.__class__ == KeyError:
                raise SeepResolvingError("We could not map your input to a valid hpo code.")
            raise e
