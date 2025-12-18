from unittest import skip
from e2e_tester import EndToEndTester
from conversational_gcode.operations.boss.CircularBoss import CircularBoss


class TestCircularBoss(EndToEndTester):

    def test_shallow_wide_origin(self):
        self.gcode_generator.add_operation(
            CircularBoss(final_diameter=26, initial_diameter=46, height=2)
        )

        self.assertFileMatches('resources/e2e/circular_boss/shallow_wide_origin.nc')

    def test_deep_narrow_position(self):
        self.gcode_generator.add_operation(
            CircularBoss(
                centre=[12, 13],
                top_height=-10,
                final_diameter=6,
                initial_diameter=10,
                height=20
            )
        )

        self.assertFileMatches('resources/e2e/circular_boss/deep_narrow_position.nc')

    @skip
    def test_deep_wide_position_finishing(self):
        self.options.tool.finishing_pass = 0.5

        # self.gcode_generator.add_operation(
        #     CircularBoss(
        #         centre=[12, 13],
        #         top_height=-10,
        #         final_diameter=26,
        #         initial_diameter=46,
        #         height=20,
        #         finishing_pass=True
        #     )
        # )
        #
        # self.assertFileMatches('resources/e2e/circular_boss/deep_wide_position_finishing.nc', True)

    @skip
    def test_deep_wide_position_finishing_conventional(self):
        self.options.tool.finishing_pass = 0.5
        self.options.tool.finishing_climb = False

        # self.gcode_generator.add_operation(
        #     CircularBoss(
        #         centre=[12, 13],
        #         top_height=-10,
        #         final_diameter=26,
        #         initial_diameter=46,
        #         height=20,
        #         finishing_pass=True
        #     )
        # )
        #
        # self.assertFileMatches('resources/e2e/circular_boss/deep_wide_position_finishing_conventional.nc', True)
