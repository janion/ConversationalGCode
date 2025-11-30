from e2e_tester import EndToEndTester
from conversational_gcode.operations.pocket.RectangularPocket import RectangularPocket


class TestRectangularPocket(EndToEndTester):

    def test_shallow_square_origin_centre(self):
        self.gcode_generator.add_operation(
            RectangularPocket(width=20, length=20, depth=2)
        )

        self.assertFileMatches('resources/e2e/rectangular_pocket/shallow_square_origin.nc')

    def test_shallow_long_origin_centre(self):
        self.gcode_generator.add_operation(
            RectangularPocket(width=20, length=30, depth=2)
        )

        self.assertFileMatches('resources/e2e/rectangular_pocket/shallow_long_origin.nc')

    def test_shallow_wide_origin_centre(self):
        self.gcode_generator.add_operation(
            RectangularPocket(width=30, length=20, depth=2)
        )

        self.assertFileMatches('resources/e2e/rectangular_pocket/shallow_wide_origin.nc')

    def test_deep_long_position_centre(self):
        self.gcode_generator.add_operation(
            RectangularPocket(width=20, length=30, depth=5, start_depth=-3, centre=[10, 20])
        )

        self.assertFileMatches('resources/e2e/rectangular_pocket/deep_long_position.nc')

    def test_deep_long_position_centre_finishing(self):
        self.options.tool.finishing_pass = 0.5

        self.gcode_generator.add_operation(
            RectangularPocket(
                width=20,
                length=30,
                depth=5,
                start_depth=-3,
                centre=[10, 20],
                finishing_pass=True
            )
        )

        self.assertFileMatches('resources/e2e/rectangular_pocket/deep_long_position_finishing.nc')

    def test_deep_long_position_centre_finishing_conventional(self):
        self.options.tool.finishing_pass = 0.5
        self.options.tool.finishing_climb = False

        self.gcode_generator.add_operation(
            RectangularPocket(
                width=20,
                length=30,
                depth=5,
                start_depth=-3,
                centre=[10, 20],
                finishing_pass=True
            )
        )

        self.assertFileMatches('resources/e2e/rectangular_pocket/deep_long_position_finishing_conventional.nc')

    def test_shallow_square_origin_corner(self):
        self.gcode_generator.add_operation(
            RectangularPocket(width=20, length=20, depth=2, corner=[-10, -10])
        )

        self.assertFileMatches('resources/e2e/rectangular_pocket/shallow_square_origin.nc')

    def test_shallow_long_origin_corner(self):
        self.gcode_generator.add_operation(
            RectangularPocket(width=20, length=30, depth=2, corner=[-10, -15])
        )

        self.assertFileMatches('resources/e2e/rectangular_pocket/shallow_long_origin.nc')

    def test_shallow_wide_origin_corner(self):
        self.gcode_generator.add_operation(
            RectangularPocket(width=30, length=20, depth=2, corner=[-15, -10])
        )

        self.assertFileMatches('resources/e2e/rectangular_pocket/shallow_wide_origin.nc')

    def test_deep_long_position_corner(self):
        self.gcode_generator.add_operation(
            RectangularPocket(width=20, length=30, depth=5, start_depth=-3, corner=[0, 5])
        )

        self.assertFileMatches('resources/e2e/rectangular_pocket/deep_long_position.nc')

    def test_deep_long_position_corner_finishing(self):
        self.options.tool.finishing_pass = 0.5

        self.gcode_generator.add_operation(
            RectangularPocket(
                width=20,
                length=30,
                depth=5,
                start_depth=-3,
                corner=[0, 5],
                finishing_pass=True
            )
        )

        self.assertFileMatches('resources/e2e/rectangular_pocket/deep_long_position_finishing.nc')

    def test_deep_long_position_corner_finishing_conventional(self):
        self.options.tool.finishing_pass = 0.5
        self.options.tool.finishing_climb = False

        self.gcode_generator.add_operation(
            RectangularPocket(
                width=20,
                length=30,
                depth=5,
                start_depth=-3,
                corner=[0, 5],
                finishing_pass=True
            )
        )

        self.assertFileMatches('resources/e2e/rectangular_pocket/deep_long_position_finishing_conventional.nc')
