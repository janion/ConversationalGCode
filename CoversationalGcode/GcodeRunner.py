from CoversationalGcode.GcodeGenerator import GcodeGenerator
from CoversationalGcode.Hole import Hole
from CoversationalGcode.Options import ToolOptions, OutputOptions

if __name__ == '__main__':
    tool_options = ToolOptions(
        tool_flutes=4,
        tool_diameter=6,  # mm
        spindle_speed=4000,  # RPM
        feed_rate=480,  # mm per min
        max_stepover=2.5,  # mm
        max_helix_stepover=2.5,  # mm
        max_stepdown=4,  # mm
        clearance_height=5,  # mm
        finishing_pass=0.3,  # mm
        finishing_feed_rate = 120 # mm per min
    )
    output_options = OutputOptions(precision=2)

    gcode_generator = GcodeGenerator(tool_options, output_options)
    gcode_generator.add_operation(Hole(0, 0, 0, 28.5, 3, True))
    commands = gcode_generator.generate()

    for command in commands:
        print(command)
