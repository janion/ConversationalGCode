from gcodes.GCodes import Comment, M2, M3, M5, G0


class CommandPrinter:

    def __init__(self, output_options):
        self.output_options = output_options
        self.commands = []

    def append(self, command):
        print(command.format(self.output_options))
        self.commands.append(command)

    def __iter__(self):
        return self.commands.__iter__()


class GcodeGenerator:

    def __init__(self, options):
        self._options = options
        self._operations = []

    def add_operation(self, operation):
        self._operations.append(operation)

    def generate(self, position=None):
        # commands = CommandPrinter()
        if position is None:
            position = [0, 0, 0]
        commands = []

        position[2] = self._options.job.clearance_height
        commands.append(G0(z=position[2], comment='Clear tool'))

        commands.append(Comment())
        commands.append(M3(s=self._options.tool.spindle_speed, comment='Start spindle'))
        commands.append(Comment())

        for operation in self._operations:
            operation.generate(position, commands, self._options)

            position[2] = self._options.job.clearance_height
            commands.append(G0(z=position[2], comment='Clear tool'))

        commands.append(Comment())
        commands.append(M5(comment='Stop spindle'))
        commands.append(M2(comment='End program'))

        return commands
