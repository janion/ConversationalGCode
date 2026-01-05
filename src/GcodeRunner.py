from conversational_gcode.GcodeGenerator import GcodeGenerator
# from conversational_gcode.operations.pocket.RectangularPocket import RectangularPocket
from conversational_gcode.operations.pocket.CircularPocket import CircularPocket
from conversational_gcode.operations.boss.CircularBoss import CircularBoss
from conversational_gcode.operations.pocket.RectangularPocket import RectangularPocket
from conversational_gcode.operations.profile.RectangularProfile import RectangularProfile
from conversational_gcode.options.Options import Options
from conversational_gcode.options.ToolOptions import ToolOptions
from conversational_gcode.options.OutputOptions import OutputOptions
from conversational_gcode.options.JobOptions import JobOptions

if __name__ == '__main__':
    tool_options = ToolOptions(
        tool_flutes=4,
        tool_diameter=8,  # mm
        spindle_speed=3180,  # RPM
        feed_rate=240,  # mm per min
        max_stepover=3,  # mm
        max_helix_stepover=3,  # mm
        helix_feed_rate=80,  # mm
        max_stepdown=3,  # mm
        finishing_pass=0.2,  # mm
        finishing_feed_rate=300,  # mm per min
        finishing_climb=True
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

    # gcode_generator.add_operation(Drill(centres=[[10, 10], [-10, 10]], depth=2, peck_interval=3))
    # gcode_generator.add_operation(Drill(centres=[[-10, -10], [-10, -5]], depth=2, dwell=3))
    # gcode_generator.add_operation(Drill(centres=[[10, -5], [5, -5]], depth=2))

    # gcode_generator.add_operation(CircularPocket(centre=[0, 0], start_depth=0, diameter=28, depth=13, finishing_pass=False))
    # gcode_generator.add_operation(CircularBoss(centre=[-9, 0], height=16, top_height=-13, initial_diameter=45, final_diameter=8, finishing_pass=False))

    # 8mm circular boss at [x, y] = [-9, 0] 3mm depth starting at 0mm
    # gcode_generator.add_operation(CircularBoss(centre=[-9, 0], height=3, top_height=0, initial_diameter=45, final_diameter=8, finishing_pass=False))


    # gcode_generator.add_operation(RectangularPocket(corner=[-5, -27], width=18, length=40, depth=13, start_depth=-6, finishing_pass=False))

    # gcode_generator.add_operation(RectangularPocket(corner=[-19, 4], width=14, length=12, depth=6, start_depth=-13, finishing_pass=False))
    # gcode_generator.add_operation(RectangularPocket(corner=[-19, -16], width=14, length=12, depth=6, start_depth=-13, finishing_pass=False))

    # gcode_generator.add_operation(CircularBoss(centre=[-9, 0], height=19, top_height=0, initial_diameter=13, final_diameter=8, finishing_pass=True))

    # gcode_generator.add_operation(RectangularProfile(centre=[0, 0], width=34, length=50, depth=11, start_depth=0, is_inner=False))

    # # Circular pocket for bearing
    # gcode_generator.add_operation(CircularPocket(centre=[25, 25], start_depth=0, diameter=40.05, depth=12.1, finishing_pass=True))
    # # Circular clearance hole for axle
    # gcode_generator.add_operation(CircularPocket(centre=[25, 25], start_depth=-12.1, diameter=30, depth=0.5, finishing_pass=False))
    # # # Circular hole for axle
    # # gcode_generator.add_operation(CircularPocket(centre=[25, 25], start_depth=-13, diameter=25, depth=(20 - 13) + 1, finishing_pass=False))
    # # Rectangular cutout for step
    # gcode_generator.add_operation(
    #     RectangularPocket(
    #         corner=[-25, -tool_options.tool_diameter / 2],
    #         width=25,
    #         length=50 + tool_options.tool_diameter,
    #         depth=2.0,
    #         start_depth=0,
    #         finishing_pass=False
    #     )
    # )

    # gcode_generator = GcodeGenerator(options)
    # gcode_generator.add_operation(CircularPocket(centre=[25, 25], start_depth=-12.0, diameter=40.05, depth=0.1, finishing_pass=True))

    # tool_options.feed_rate = 120
    # gcode_generator = GcodeGenerator(options)
    #
    # # Rectangular profile for outline
    # gcode_generator.add_operation(
    #     RectangularProfile(
    #         corner=[-25, 0],
    #         width=75,
    #         length=50,
    #         depth=6.0,
    #         start_depth=0,
    #         is_inner=False
    #     )
    # )


    # Rectangular cutout for step
    gcode_generator.add_operation(
        RectangularPocket(
            centre=[0, 0],
            width=50.5,
            length=25 + tool_options.tool_diameter,
            depth=2.0,
            start_depth=0,
            finishing_pass=False
        )
    )

    commands = gcode_generator.generate()

    for command in commands:
        print(command.format(output_options))

    # # Cut to square off bottom edge
    # print(f'G0 Z{job_options.clearance_height}')
    # print(f'G0 X-{25 + tool_options.tool_diameter / 2} Y{20 + tool_options.tool_diameter / 2}')
    # print(f'G0 Z-21')
    # print(f'G1 X-{25 + tool_options.tool_diameter / 2} Y-{20 + tool_options.tool_diameter / 2} F{tool_options.feed_rate}')
    # print(f'G0 Z{job_options.clearance_height}')

    # OutputOptions(**json.loads(json.dumps(dict(oo))))
