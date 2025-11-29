"""
Options for GCode generation.

Classes:
- Options
  - Options for GCode generation. Contains sub-objects for more specific options.
"""

from conversational_gcode.options.ToolOptions import ToolOptions
from conversational_gcode.options.JobOptions import JobOptions
from conversational_gcode.options.OutputOptions import OutputOptions
from conversational_gcode.validate.validation_result import ValidationResult
from conversational_gcode.Jsonable import Jsonable


class Options(Jsonable):
    """
    Options for GCode generation. Contains sub-objects for more specific options.

    Attributes:
        tool (ToolOptions): ToolOptions defining options for a cutting tool.
        job (JobOptions): JobOptions for defining options for the whole job.
        output (OutputOptions): OutputOptions for defining options relating to printing the GCode.
    """

    def __init__(
            self,
            tool: ToolOptions = None,
            job: JobOptions = None,
            output: OutputOptions = None
    ):
        """
        Initialise the options.

        :param tool: ToolOptions defining options for a cutting tool.
        :param job: JobOptions for defining options for the whole job.
        :param output: OutputOptions for defining options relating to printing the GCode.
        """
        self._tool = tool if tool is not None else ToolOptions()
        self._job = job if job is not None else JobOptions()
        self._output = output if output is not None else OutputOptions()

    def validate(self):
        results = []
        results.extend(self._output.validate())
        results.extend(self._job.validate())
        results.extend(self._tool.validate())

        results = list(filter(lambda result: not result.success, results))

        if len(results) == 0:
            results.append(ValidationResult())

        return results

    tool = property(fget=lambda self: self._tool)
    job = property(fget=lambda self: self._job)
    output = property(fget=lambda self: self._output)
