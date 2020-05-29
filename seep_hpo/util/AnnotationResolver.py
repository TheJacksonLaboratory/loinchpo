from seep_hpo.errors.SeepValidationError import SeepValidationError
from seep_hpo.errors.SeepResolvingError import SeepResolvingError


class AnnotationResolver:
    def __init__(self, annotations):
        self.annotations = annotations

    def resolve(self, query):
        try:
            # Transform inputs into expectations
            return self.annotations[query.loinc_id][query.measure][query.negated]
        except (KeyError, SeepValidationError) as e:
            if e.__class__ == KeyError:
                raise SeepResolvingError("We could not map your input to a valid hpo code.")
            raise e
