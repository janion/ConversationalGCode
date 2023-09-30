from src.GcodeGenerator import GcodeGenerator
from src.CircularPocket import CircularPocket
from src.Options import Options, ToolOptions, OutputOptions, JobOptions

if __name__ == '__main__':
    tool_options = ToolOptions(
        tool_flutes=4,
        tool_diameter=6,  # mm
        spindle_speed=4000,  # RPM
        feed_rate=480,  # mm per min
        max_stepover=2.5,  # mm
        max_helix_stepover=2.5,  # mm
        max_stepdown=4,  # mm
        finishing_pass=0.3,  # mm
        finishing_feed_rate=120  # mm per min
    )
    job_options = JobOptions(
        clearance_height=5,  # mm
    )
    output_options = OutputOptions()
    options = Options(tool_options, job_options, output_options)

    gcode_generator = GcodeGenerator(options)
    # gcode_generator.add_operation(CircularPocket(0, 0, 0, 8, 9, True))
    gcode_generator.add_operation(CircularPocket(0, 0, 0, 26, 9, True))
    # gcode_generator.add_operation(CircularPocket(0, 0, 0, 8, 9, False))
    # gcode_generator.add_operation(CircularPocket(0, 0, 0, 26, 9, False))
    # gcode_generator.add_operation(CircularPocket(0, 0, 0, 8, 2, True))
    # gcode_generator.add_operation(CircularPocket(0, 0, 0, 26, 2, True))
    # gcode_generator.add_operation(CircularPocket(0, 0, 0, 8, 2, False))
    # gcode_generator.add_operation(CircularPocket(0, 0, 0, 26, 2, False))
    commands = gcode_generator.generate()

    for command in commands:
        print(command.format(output_options))
