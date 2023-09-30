from gcodes.GCodes import M2, M3, M5, G0


class _CommandPrinter:

    def append(self, command):
        print(command)


class GcodeGenerator:

    def __init__(self, options):
        self._options = options
        self._operations = []

    def add_operation(self, operation):
        self._operations.append(operation)

    def generate(self):
        # commands = _CommandPrinter()
        commands = []
        position = [0, 0, 0]

        position[2] = self._options.job.clearance_height
        commands.append(G0(z=position[2], comment='Clear tool'))

        commands.append('')
        commands.append(M3(s=self._options.tool.spindle_speed, comment='Start spindle'))
        commands.append('')

        for operation in self._operations:
            operation.generate(position, commands, self._options)

            position[2] = self._options.job.clearance_height
            commands.append(G0(z=position[2], comment='Clear tool'))

        commands.append('')
        commands.append(M5(comment='Stop spindle'))
        commands.append(M2(comment='End program'))

        return commands
