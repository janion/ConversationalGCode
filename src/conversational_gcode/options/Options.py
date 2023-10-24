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
    """

    def __init__(self, tool: ToolOptions, job: JobOptions, output: OutputOptions):
        """
        Initialise the options.

        This will throw a ValueError if any argument is None.
        :param tool: ToolOptiopns defining options for a cutting tool.
        :param job: JobOptions for defining options for the whole job.
        :param output: OutputOptions for defining options relating to printing the GCode.
        """
        if tool is None:
            raise ValueError('Tool options must be populated')
        elif job is None:
            raise ValueError('Job options must be populated')
        elif output is None:
            raise ValueError('Output options must be populated')

        self._tool = tool
        self._job = job
        self._output = output

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
