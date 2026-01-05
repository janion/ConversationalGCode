from conversational_gcode.gcodes.GCodes import GCode
from conversational_gcode.options.Options import Options


class Operation:

    def validate(self, options=None):
        raise NotImplementedError

    def generate(self, position: list[float], commands: list[GCode], options: Options) -> None:
        raise NotImplementedError
