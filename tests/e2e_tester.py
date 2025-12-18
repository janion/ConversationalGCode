from unittest import TestCase
from os.path import join, dirname
from conversational_gcode.GcodeGenerator import GcodeGenerator
from conversational_gcode.options.Options import Options


class EndToEndTester(TestCase):

    def setUp(self):
        self.options = Options()
        self.gcode_generator = GcodeGenerator(self.options)

    def assertFileMatches(self, filepath: str, write_reference: bool = False):
        generated_commands = [command.format(self.options.output) for command in self.gcode_generator.generate()]

        full_filepath = join(dirname(__file__), filepath)

        if write_reference:
            with open(full_filepath, 'w') as reference_file:
                reference_file.write('\n'.join(generated_commands))
            self.fail()

        reference_commands = []
        with open(full_filepath, 'r') as reference_file:
            while line := reference_file.readline():
                reference_commands.append(line.rstrip())

        self.assertEqual(len(reference_commands), len(generated_commands))

        for index in range(len(reference_commands)):
            self.assertEqual(
                reference_commands[index],
                generated_commands[index]
            )
