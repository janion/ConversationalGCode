"""
Options related to an entire job.

Classes:
- JobOptions
  - Options for a job.
"""

from conversational_gcode.validate.validation_result import ValidationResult
from conversational_gcode.Jsonable import Jsonable


class JobOptions(Jsonable):
    """
    Options for a job.
    """

    def __init__(self, clearance_height: float = 10, lead_in: float = 0.25):
        """
        Initialise the job options.
        :param clearance_height: Height at which the tool is guaranteed to be clear of the work. Defaults to 10mm.
        :param lead_in: Height above the work surface to start plunge operations. Defaults to 0.25mm.
        """
        self._clearance_height = clearance_height
        self._lead_in = lead_in

    def validate(self):
        results = []
        if self._clearance_height is None or self._clearance_height <= 0:
            results.append(ValidationResult(False, 'Clearance height must be greater than zero'))
        if self._lead_in is None or self._lead_in < 0:
            results.append(ValidationResult(False, 'Lead-in must be positive or zero'))

        if len(results) == 0:
            results.append(ValidationResult())

        return results

    def _set_clearance_height(self, value):
        self._clearance_height = value

    def _set_lead_in(self, value):
        self._lead_in = value

    clearance_height = property(
        fget=lambda self: self._clearance_height,
        fset=_set_clearance_height
    )

    lead_in = property(
        fget=lambda self: self._lead_in,
        fset=_set_lead_in
    )
