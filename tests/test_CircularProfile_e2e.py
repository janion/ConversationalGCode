from unittest import skip
from e2e_tester import EndToEndTester
from conversational_gcode.operations.profile.CircularProfile import CircularProfile


class TestCircularProfile(EndToEndTester):

    def test_shallow_wide_origin(self):
        self.gcode_generator.add_operation(
            CircularProfile(diameter=26, depth=2)
        )

        self.assertFileMatches('resources/e2e/circular_profile/shallow_wide_origin.nc')

    def test_deep_narrow_position(self):
        self.gcode_generator.add_operation(
            CircularProfile(
                centre=(12, 13),
                start_depth=-10,
                diameter=self.options.tool.tool_diameter + self.options.tool.max_helix_stepover * 2,
                depth=20
            )
        )

        self.assertFileMatches('resources/e2e/circular_profile/deep_narrow_position.nc')

    @skip
    def test_deep_wide_position_finishing(self):
        self.options.tool.finishing_pass = 0.5

        # self.gcode_generator.add_operation(
        #     CircularProfile(
        #         centre=(12, 13),
        #         start_depth=-10,
        #         diameter=26,
        #         depth=20,
        #         finishing_pass=True
        #     )
        # )
        #
        # self.assertFileMatches('resources/e2e/circular_profile/deep_wide_position_finishing.nc', True)

    @skip
    def test_deep_wide_position_finishing_conventional(self):
        self.options.tool.finishing_pass = 0.5
        self.options.tool.finishing_climb = False

        # self.gcode_generator.add_operation(
        #     CircularProfile(
        #         centre=(12, 13),
        #         start_depth=-10,
        #         diameter=26,
        #         depth=20,
        #         finishing_pass=True
        #     )
        # )
        #
        # self.assertFileMatches('resources/e2e/circular_profile/deep_wide_position_finishing_conventional.nc', True)
