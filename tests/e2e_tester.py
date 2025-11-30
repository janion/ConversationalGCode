from unittest import TestCase
from conversational_gcode.GcodeGenerator import GcodeGenerator
from conversational_gcode.options.Options import Options


class EndToEndTester(TestCase):

    def setUp(self):
        self.options = Options()
        self.gcode_generator = GcodeGenerator(self.options)

    def assertFileMatches(self, filepath: str, print_generated: bool = False):
        reference_commands = []
        with open(filepath, 'r') as reference_file:
            while line := reference_file.readline():
                reference_commands.append(line.rstrip())

        generated_commands = [command.format(self.options.output) for command in self.gcode_generator.generate()]

        if print_generated:
            for command in generated_commands:
                print(command)

        self.assertEqual(len(reference_commands), len(generated_commands))

        for index in range(len(reference_commands)):
            self.assertEqual(
                reference_commands[index],
                generated_commands[index]
            )
