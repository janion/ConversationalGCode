from conversational_gcode.gcodes.GCodes import GCode
from conversational_gcode.options.Options import Options
from conversational_gcode.position.Position import Position


class Operation:

    def validate(self, options=None):
        raise NotImplementedError

    def generate(self, position: Position, commands: list[GCode], options: Options) -> None:
        raise NotImplementedError
