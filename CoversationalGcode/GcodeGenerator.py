

class _CommandPrinter:

    def append(self, command):
        print(command)

class GcodeGenerator:

    def __init__(self, tool_options, output_options):
        self._tool_options = tool_options
        self._output_options = output_options
        self._operations = []

    def add_operation(self, operation):
        self._operations.append(operation)

    def generate(self):
        # commands = _CommandPrinter()
        commands = []
        position = [0, 0, 0]

        position[2] = self._tool_options.clearance_height
        commands.append(f'G0 Z{position[2]}; Clear tool')

        commands.append('')
        commands.append(f'M03 S{self._tool_options.spindle_speed:.{self._output_options.precision}f}; Start spindle')
        commands.append('')

        for operation in self._operations:
            operation.generate(position, commands, self._tool_options, self._output_options)

            position[2] = self._tool_options.clearance_height
            commands.append(f'G0 Z{position[2]}; Clear tool')

        commands.append('')
        commands.append('M05; Stop spindle')
        commands.append('M02; End program')

        return commands
