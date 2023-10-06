from operations.Operations import helical_plunge
from gcodes.GCodes import Comment, G0, G80, G81, G82, G83, CyclePosition


class Drill:

    def __init__(self,
                 centres: list,
                 depth: float,
                 start_depth: float = 0,
                 peck_interval: float = None,
                 dwell: float = None):
        if centres is None or centres == []:
            raise ValueError('Drill centre coordinates must be specified')
        elif start_depth is None:
            raise ValueError('Drill start depth must be specified')
        elif depth is None or depth <= 0:
            raise ValueError('Drill depth must be positive and non-zero')
        elif peck_interval is not None and peck_interval < 0:
            raise ValueError('Drill peck interval must be None, zero or positive')
        elif dwell is not None and dwell < 0:
            raise ValueError('Drill dwell must be None, zero or positive')

        if peck_interval is not None and peck_interval > 0 and dwell is not None and dwell > 0:
            raise ValueError('No drilling operation supports both pecking and a dwell. Please choose one or none.')

        self._centres = centres

        if peck_interval is not None and peck_interval > 0:
            self._command = lambda r, f, comment=None: G83(z=start_depth - depth, r=r, i=peck_interval, f=f, comment=comment)
        elif dwell is not None and dwell > 0:
            self._command = lambda r, f, comment=None: G82(z=start_depth - depth, r=r, p=dwell, f=f, comment=comment)
        else:
            self._command = lambda r, f, comment=None: G81(z=start_depth - depth, r=r, f=f, comment=comment)

    def generate(self, position, commands, options):
        # Setup
        tool_options = options.tool
        job_options = options.job

        # Position tool
        position[0] = self._centres[0][0]
        position[1] = self._centres[0][1]
        commands.append(G0(x=position[0], y=position[1], comment='Move to starting position'))
        commands.append(self._command(r=job_options.lead_in, f=tool_options.feed_rate, comment='Start drilling cycle'))

        for centre in self._centres[1:]:
            position[0] = centre[0]
            position[1] = centre[1]
            commands.append(CyclePosition(x=position[0], y=position[1]))

        commands.append(G80(comment='End drilling cycle'))
        commands.append(Comment(''))
