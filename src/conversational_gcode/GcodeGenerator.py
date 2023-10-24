"""
Generates GCode from configures objects.

Classes:
- _CommandPrinter
  - Debugging tool to print commands as they are added to the list.
- GcodeGenerator
  - Iterates through configured operations and collates the GCode commands.
"""

from conversational_gcode.options.OutputOptions import OutputOptions
from conversational_gcode.options.Options import Options
from conversational_gcode.validate.validation_result import ValidationResult
from conversational_gcode.gcodes.GCodes import GCode, M2, M3, M5, G0


class _CommandPrinter:
    """
    Debugging tool to print commands as they are added to the list.
    """

    def __init__(self, output_options: OutputOptions):
        """
        Initialise the printer.
        :param output_options: OutputOptions to define how to format the printed output.
        """
        self.output_options = output_options
        self.commands = []

    def append(self, command):
        print(command.format(self.output_options))
        self.commands.append(command)

    def extend(self, commands):
        for command in commands:
            print(command.format(self.output_options))
        self.commands.extend(commands)

    def __iter__(self):
        return [].__iter__()


class GcodeGenerator:
    """
    Iterates through configured operations and collates the GCode commands.
    """

    def __init__(self, options: Options):
        """
        Initialise the generator.
        :param options: Options for the generation.
        """
        self._options = options
        self._operations = []

    def add_operation(self, operation):
        """
        Add an operation to the list.
        :param operation: Operation to add.
        :return: None.
        """
        self._operations.append(operation)

    def _validate(self) -> list[ValidationResult]:
        """
        Validate the operations and options.
        :return: List of ValidationResults. Contains only 1 item if every option and operation is valid.
        """
        results = []
        results.extend(self._options.validate())
        for op in self._operations:
            results.extend(op.validate(self._options))

        results = list(filter(lambda result: not result.success, results))

        if len(results) == 0:
            results.append(ValidationResult())

        return results

    def generate(self, position: list[float] = None) -> list[GCode]:
        """
        Generate the GCode for all of the operations.
        :param position: Starting position of the job. Defaults to None to start at [0, 0, 0]
        :return: List of generated GCode commands
        """
        results = self._validate()

        if len(results) > 1 or not results[0].success:
            return [result.message for result in results]

        if position is None:
            position = [0, 0, 0]
        # commands = CommandPrinter(self._options.output)
        commands = []

        position[2] = self._options.job.clearance_height
        commands.append(G0(z=position[2], comment='Clear tool'))

        commands.append(GCode())
        commands.append(M3(s=self._options.tool.spindle_speed, comment='Start spindle'))
        commands.append(GCode())

        for operation in self._operations:
            operation.generate(position, commands, self._options)

            position[2] = self._options.job.clearance_height
            commands.append(G0(z=position[2], comment='Clear tool'))
            commands.append(GCode())

        commands.append(M5(comment='Stop spindle'))
        commands.append(M2(comment='End program'))

        return commands
