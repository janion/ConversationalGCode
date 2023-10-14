from conversational_gcode.validate.validation_result import ValidationResult
from conversational_gcode.gcodes.GCodes import Comment, G80, G81, G82, G83, CyclePosition


class Drill:

    def __init__(self,
                 centres: list = None,
                 depth: float = 3,
                 start_depth: float = 0,
                 peck_interval: float = None,
                 dwell: float = None):
        self._centres = [] if centres is None else centres
        self._depth = depth
        self._start_depth = start_depth
        self._peck_interval = peck_interval
        self._dwell = dwell

    def validate(self, options = None):
        results = []
        if self._centres is None or self._centres == []:
            results.append(ValidationResult(False, 'Drill centre coordinates must be specified'))
        if self._start_depth is None:
            results.append(ValidationResult(False, 'Drill start depth must be specified'))
        if self._depth is None or self._depth <= 0:
            results.append(ValidationResult(False, 'Drill depth must be positive and non-zero'))
        if self._peck_interval is not None and self._peck_interval < 0:
            results.append(ValidationResult(False, 'Drill peck interval must be None, zero or positive'))
        if self._dwell is not None and self._dwell < 0:
            results.append(ValidationResult(False, 'Drill dwell must be None, zero or positive'))

        if self._peck_interval is not None and self._peck_interval > 0 and self._dwell is not None and self._dwell > 0:
            results.append(ValidationResult(False, 'No drilling operation supports both pecking and a dwell. Please choose one or none.'))
        
        if len(results) == 0:
            results.append(ValidationResult())

        return results

    def _set_centres(self, value):
        self._centres = value

    def _set_depth(self, value):
        self._depth = value

    def _set_start_depth(self, value):
        self._start_depth = value

    def _set_peck_interval(self, value):
        self._peck_interval = value

    def _set_dwell(self, value):
        self._dwell = value

    centres = property(
        fget=lambda self: self._centres,
        fset=_set_centres
    )
    depth = property(
        fget=lambda self: self._depth,
        fset=_set_depth
    )
    start_depth = property(
        fget=lambda self: self._start_depth,
        fset=_set_start_depth
    )
    peck_interval = property(
        fget=lambda self: self._peck_interval,
        fset=_set_peck_interval
    )
    dwell = property(
        fget=lambda self: self._dwell,
        fset=_set_dwell
    )

    def generate(self, position, commands, options):
        # Setup
        tool_options = options.tool
        job_options = options.job

        # Position tool
        position[0] = self._centres[0][0]
        position[1] = self._centres[0][1]

        if self._peck_interval is not None and self._peck_interval > 0:
            def drill_command(x, y, r, f, comment=None):
                return G83(x=x, y=y, z=self._start_depth - self._depth, r=r, i=self._peck_interval, f=f, comment=comment)
        elif self._dwell is not None and self._dwell > 0:
            def drill_command(x, y, r, f, comment=None):
                return G82(x=x, y=y, z=self._start_depth - self._depth, r=r, p=self._dwell, f=f, comment=comment)
        else:
            def drill_command(x, y, r, f, comment=None):
                return G81(x=x, y=y, z=self._start_depth - self._depth, r=r, f=f, comment=comment)

        commands.append(drill_command(x=position[0], y=position[1], r=job_options.lead_in, f=tool_options.feed_rate, comment='Start drilling cycle'))

        for centre in self._centres[1:]:
            position[0] = centre[0]
            position[1] = centre[1]
            commands.append(CyclePosition(x=position[0], y=position[1]))

        commands.append(G80(comment='End drilling cycle'))
        commands.append(Comment(''))
