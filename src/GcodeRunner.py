from src.GcodeGenerator import GcodeGenerator
from operations.CircularPocket import CircularPocket
from operations.CircularProfile import CircularProfile
from operations.Drill import Drill
from operations.RectangularPocket import RectangularPocket
from operations.RectangularProfile import RectangularProfile
from options.Options import Options, ToolOptions, OutputOptions, JobOptions

if __name__ == '__main__':
    tool_options = ToolOptions(
        tool_flutes=4,
        tool_diameter=8,  # mm
        spindle_speed=4000,  # RPM
        feed_rate=400,  # mm per min
        max_stepover=2,  # mm
        max_helix_stepover=2,  # mm
        max_stepdown=3,  # mm
        finishing_pass=0.3,  # mm
        finishing_feed_rate=100  # mm per min
    )
    job_options = JobOptions(
        clearance_height=10  # mm
    )
    output_options = OutputOptions()
    options = Options(tool_options, job_options, output_options)

    gcode_generator = GcodeGenerator(options)
    # gcode_generator.add_operation(CircularPocket(centre=[0, 0], start_depth=0, diameter=18, depth=2, finishing_pass=True))
    # gcode_generator.add_operation(CircularPocket(centre=[0, 0], start_depth=0, diameter=26, depth=9, finishing_pass=True))
    # gcode_generator.add_operation(CircularPocket(centre=[0, 0], start_depth=0, diameter=8, depth=9, finishing_pass=False))
    # gcode_generator.add_operation(CircularPocket(centre=[0, 0], start_depth=0, diameter=26, depth=9, finishing_pass=False))
    # gcode_generator.add_operation(CircularPocket(centre=[0, 0], start_depth=0, diameter=8, depth=2, finishing_pass=True))
    # gcode_generator.add_operation(CircularPocket(centre=[0, 0], start_depth=0, diameter=26, depth=2, finishing_pass=True))
    # gcode_generator.add_operation(CircularPocket(centre=[0, 0], start_depth=0, diameter=8, depth=2, finishing_pass=False))
    # gcode_generator.add_operation(CircularPocket(centre=[0, 0], start_depth=0, diameter=26, depth=2, finishing_pass=False))

    # gcode_generator.add_operation(CircularProfile(centre=[0, 0], start_depth=-10, diameter=26, depth=20, is_inner=False))

    # gcode_generator.add_operation(RectangularPocket(centre=[10, 10], width=22, length=32, depth=0.5))
    # gcode_generator.add_operation(RectangularPocket(centre=[0, 0], width=32, length=22, depth=0.5))
    # gcode_generator.add_operation(RectangularPocket(centre=[10, 10], width=22, length=32, depth=0.5))
    # gcode_generator.add_operation(RectangularPocket(centre=[10, 10], width=32, length=22, depth=0.5))

    # gcode_generator.add_operation(RectangularPocket(centre=[0, 0], width=70, length=40, depth=2, finishing_pass=True))
    # gcode_generator.add_operation(RectangularPocket(centre=[10, 10], width=32, length=22, depth=2, finishing_pass=True))

    # gcode_generator.add_operation(RectangularProfile(centre=[10, 10], width=32, length=22, depth=2, is_inner=False))

    gcode_generator.add_operation(Drill(centres=[[10, 10], [-10, 10]], depth=2, peck_interval=3))
    gcode_generator.add_operation(Drill(centres=[[-10, -10], [-10, -5]], depth=2, dwell=3))
    gcode_generator.add_operation(Drill(centres=[[10, -5], [5, -5]], depth=2))

    position = [0, 0, 0]
    commands = gcode_generator.generate(position=position)

    for command in commands:
        print(command.format(output_options))

    print(f'\nFinal position: {position}')
