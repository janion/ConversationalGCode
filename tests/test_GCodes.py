from unittest import TestCase

from conversational_gcode.options.OutputOptions import OutputOptions
from conversational_gcode.gcodes.GCodes import *


class TestCode(TestCase):

    def setUp(self):
        self.output_options = OutputOptions()
        self.comment = "I am a comment, I am"
        self.speed = 42
        self.x = 10
        self.y = 101
        self.z = 1001
        self.i = 1
        self.j = 11
        self.k = 111
        self.r = 2
        self.q = 4
        self.p = 8
        self.f = 42

        self.x_coord = f'X{self.x:.{self.output_options.position_precision}f}'
        self.y_coord = f'Y{self.y:.{self.output_options.position_precision}f}'
        self.z_coord = f'Z{self.z:.{self.output_options.position_precision}f}'
        self.i_coord = f'I{self.i:.{self.output_options.position_precision}f}'
        self.j_coord = f'J{self.j:.{self.output_options.position_precision}f}'
        self.k_coord = f'K{self.k:.{self.output_options.position_precision}f}'
        self.r_coord = f'R{self.r:.{self.output_options.position_precision}f}'
        self.q_coord = f'Q{self.q:.{self.output_options.position_precision}f}'
        self.p_time = f'P{self.p:d}'
        self.feed_element = f'F{self.f:.{self.output_options.feed_precision}f}'


class TestGCode(TestCode):

    def test_gcode_without_comment(self):
        system_under_test = GCode()
        self.assertEqual(';', system_under_test.format(self.output_options))

    def test_gcode_with_comment(self):
        system_under_test = GCode(self.comment)
        self.assertEqual(f'; {self.comment}', system_under_test.format(self.output_options))

    def test_equality(self):
        expected = GCode(self.comment)
        actual = GCode(self.comment)
        self.assertEqual(expected, actual)

    def test_inequality(self):
        expected = GCode(self.comment)
        actual = GCode(f'not {self.comment}')
        self.assertNotEqual(expected, actual)


class TestM2(TestCode):

    def test_m2_without_comment(self):
        system_under_test = M2()
        self.assertEqual('M2;', system_under_test.format(self.output_options))

    def test_m2_with_comment(self):
        system_under_test = M2(self.comment)
        self.assertEqual(
            f'M2; {self.comment}',
            system_under_test.format(self.output_options)
        )

    def test_equality(self):
        expected = M2(self.comment)
        actual = M2(self.comment)
        self.assertEqual(expected, actual)

    def test_inequality(self):
        expected = M2(self.comment)
        actual = M2(f'not {self.comment}')
        self.assertNotEqual(expected, actual)


class TestM3(TestCode):

    def test_m3_without_comment(self):
        system_under_test = M3(s=self.speed)
        self.assertEqual(
            f'M3 S{self.speed:.{self.output_options.speed_precision}f};',
            system_under_test.format(self.output_options)
        )

    def test_m3_with_comment(self):
        system_under_test = M3(s=self.speed, comment=self.comment)
        self.assertEqual(
            f'M3 S{self.speed:.{self.output_options.speed_precision}f}; {self.comment}',
            system_under_test.format(self.output_options)
        )

    def test_equality(self):
        expected = M3(s=self.speed, comment=self.comment)
        actual = M3(s=self.speed, comment=self.comment)
        self.assertEqual(expected, actual)

    def test_inequality(self):
        expected = M3(s=self.speed, comment=self.comment)
        actual = M3(s=self.speed + 1, comment=self.comment)
        self.assertNotEqual(expected, actual)


class TestM5(TestCode):

    def test_m5_without_comment(self):
        system_under_test = M5()
        self.assertEqual('M5;', system_under_test.format(self.output_options))

    def test_m5_with_comment(self):
        system_under_test = M5(self.comment)
        self.assertEqual(
            f'M5; {self.comment}',
            system_under_test.format(self.output_options)
        )

    def test_equality(self):
        expected = M5(self.comment)
        actual = M5(self.comment)
        self.assertEqual(expected, actual)

    def test_inequality(self):
        expected = M5(self.comment)
        actual = M5(f'not {self.comment}')
        self.assertNotEqual(expected, actual)


class TestG0(TestCode):

    def test_g0_without_comment(self):
        system_under_test = G0(x=self.x, y=self.y, z=self.z)
        self.assertEqual(
            f'G0 {self.x_coord} {self.y_coord} {self.z_coord};',
            system_under_test.format(self.output_options)
        )

    def test_g0_with_comment(self):
        system_under_test = G0(x=self.x, y=self.y, z=self.z, comment=self.comment)
        self.assertEqual(
            f'G0 {self.x_coord} {self.y_coord} {self.z_coord}; {self.comment}',
            system_under_test.format(self.output_options)
        )

    def test_g0_without_x(self):
        system_under_test = G0(y=self.y, z=self.z)
        self.assertEqual(
            f'G0 {self.y_coord} {self.z_coord};',
            system_under_test.format(self.output_options)
        )

    def test_g0_without_y(self):
        system_under_test = G0(x=self.x, z=self.z)
        self.assertEqual(
            f'G0 {self.x_coord} {self.z_coord};',
            system_under_test.format(self.output_options)
        )

    def test_g0_without_z(self):
        system_under_test = G0(x=self.x, y=self.y)
        self.assertEqual(
            f'G0 {self.x_coord} {self.y_coord};',
            system_under_test.format(self.output_options)
        )

    def test_g0_without_x_or_y(self):
        system_under_test = G0(z=self.z)
        self.assertEqual(
            f'G0 {self.z_coord};',
            system_under_test.format(self.output_options)
        )

    def test_g0_without_x_or_z(self):
        system_under_test = G0(y=self.y)
        self.assertEqual(
            f'G0 {self.y_coord};',
            system_under_test.format(self.output_options)
        )

    def test_g0_without_y_or_z(self):
        system_under_test = G0(x=self.x)
        self.assertEqual(
            f'G0 {self.x_coord};',
            system_under_test.format(self.output_options)
        )

    def test_equality(self):
        expected = G0(x=self.x, y=self.y, z=self.z)
        actual = G0(x=self.x, y=self.y, z=self.z)
        self.assertEqual(expected, actual)

    def test_inequality(self):
        expected = G0(x=self.x, y=self.y, z=self.z)
        actual = G0(x=self.x, y=self.y, z=self.z + 1)
        self.assertNotEqual(expected, actual)


class TestG1(TestCode):

    def test_g1_without_comment(self):
        system_under_test = G1(x=self.x, y=self.y, z=self.z, f=self.f)
        self.assertEqual(
            f'G1 {self.x_coord} {self.y_coord} {self.z_coord} {self.feed_element};',
            system_under_test.format(self.output_options)
        )

    def test_g1_with_comment(self):
        system_under_test = G1(x=self.x, y=self.y, z=self.z, f=self.f, comment=self.comment)
        self.assertEqual(
            f'G1 {self.x_coord} {self.y_coord} {self.z_coord} {self.feed_element}; {self.comment}',
            system_under_test.format(self.output_options)
        )

    def test_g1_without_x(self):
        system_under_test = G1(y=self.y, z=self.z, f=self.f)
        self.assertEqual(
            f'G1 {self.y_coord} {self.z_coord} {self.feed_element};',
            system_under_test.format(self.output_options)
        )

    def test_g1_without_y(self):
        system_under_test = G1(x=self.x, z=self.z, f=self.f)
        self.assertEqual(
            f'G1 {self.x_coord} {self.z_coord} {self.feed_element};',
            system_under_test.format(self.output_options)
        )

    def test_g1_without_z(self):
        system_under_test = G1(x=self.x, y=self.y, f=self.f)
        self.assertEqual(
            f'G1 {self.x_coord} {self.y_coord} {self.feed_element};',
            system_under_test.format(self.output_options)
        )

    def test_g1_without_x_or_y(self):
        system_under_test = G1(z=self.z, f=self.f)
        self.assertEqual(
            f'G1 {self.z_coord} {self.feed_element};',
            system_under_test.format(self.output_options)
        )

    def test_g1_without_x_or_z(self):
        system_under_test = G1(y=self.y, f=self.f)
        self.assertEqual(
            f'G1 {self.y_coord} {self.feed_element};',
            system_under_test.format(self.output_options)
        )

    def test_g1_without_y_or_z(self):
        system_under_test = G1(x=self.x, f=self.f)
        self.assertEqual(
            f'G1 {self.x_coord} {self.feed_element};',
            system_under_test.format(self.output_options)
        )

    def test_equality(self):
        expected = G1(x=self.x, y=self.y, z=self.z, f=self.f)
        actual = G1(x=self.x, y=self.y, z=self.z, f=self.f)
        self.assertEqual(expected, actual)

    def test_inequality(self):
        expected = G1(x=self.x, y=self.y, z=self.z, f=self.f)
        actual = G1(x=self.x, y=self.y, z=self.z, f=self.f + 1)
        self.assertNotEqual(expected, actual)


class TestG2(TestCode):

    def setUp(self, command: type = G2, command_name: str = 'G2'):
        super().setUp()
        self.command = command
        self.command_name = command_name

    def test_arc_without_comment(self):
        system_under_test = self.command(
            x=self.x,
            y=self.y,
            z=self.z,
            i=self.i,
            j=self.j,
            k=self.k,
            f=self.f
        )
        self.assertEqual(
            f'{self.command_name} {self.x_coord} {self.y_coord} {self.z_coord} {self.i_coord} {self.j_coord} {self.k_coord} {self.feed_element};',
            system_under_test.format(self.output_options)
        )

    def test_arc_with_comment(self):
        system_under_test = self.command(
            x=self.x,
            y=self.y,
            z=self.z,
            i=self.i,
            j=self.j,
            k=self.k,
            f=self.f,
            comment=self.comment
        )
        self.assertEqual(
            f'{self.command_name} {self.x_coord} {self.y_coord} {self.z_coord} {self.i_coord} {self.j_coord} {self.k_coord} {self.feed_element}; {self.comment}',
            system_under_test.format(self.output_options)
        )

    def test_arc_without_x(self):
        system_under_test = self.command(
            y=self.y,
            z=self.z,
            i=self.i,
            j=self.j,
            k=self.k,
            f=self.f
        )
        self.assertEqual(
            f'{self.command_name} {self.y_coord} {self.z_coord} {self.i_coord} {self.j_coord} {self.k_coord} {self.feed_element};',
            system_under_test.format(self.output_options)
        )

    def test_arc_without_y(self):
        system_under_test = self.command(
            x=self.x,
            z=self.z,
            i=self.i,
            j=self.j,
            k=self.k,
            f=self.f
        )
        self.assertEqual(
            f'{self.command_name} {self.x_coord} {self.z_coord} {self.i_coord} {self.j_coord} {self.k_coord} {self.feed_element};',
            system_under_test.format(self.output_options)
        )

    def test_arc_without_z(self):
        system_under_test = self.command(
            x=self.x,
            y=self.y,
            i=self.i,
            j=self.j,
            k=self.k,
            f=self.f
        )
        self.assertEqual(
            f'{self.command_name} {self.x_coord} {self.y_coord} {self.i_coord} {self.j_coord} {self.k_coord} {self.feed_element};',
            system_under_test.format(self.output_options)
        )

    def test_arc_without_i(self):
        system_under_test = self.command(
            x=self.x,
            y=self.y,
            z=self.z,
            j=self.j,
            k=self.k,
            f=self.f
        )
        self.assertEqual(
            f'{self.command_name} {self.x_coord} {self.y_coord} {self.z_coord} {self.j_coord} {self.k_coord} {self.feed_element};',
            system_under_test.format(self.output_options)
        )

    def test_arc_without_j(self):
        system_under_test = self.command(
            x=self.x,
            y=self.y,
            z=self.z,
            i=self.i,
            k=self.k,
            f=self.f
        )
        self.assertEqual(
            f'{self.command_name} {self.x_coord} {self.y_coord} {self.z_coord} {self.i_coord} {self.k_coord} {self.feed_element};',
            system_under_test.format(self.output_options)
        )

    def test_arc_without_k(self):
        system_under_test = self.command(
            x=self.x,
            y=self.y,
            z=self.z,
            i=self.i,
            j=self.j,
            f=self.f
        )
        self.assertEqual(
            f'{self.command_name} {self.x_coord} {self.y_coord} {self.z_coord} {self.i_coord} {self.j_coord} {self.feed_element};',
            system_under_test.format(self.output_options)
        )

    def test_equality(self):
        expected = self.command(
            x=self.x,
            y=self.y,
            z=self.z,
            i=self.i,
            j=self.j,
            f=self.f
        )
        actual = self.command(
            x=self.x,
            y=self.y,
            z=self.z,
            i=self.i,
            j=self.j,
            f=self.f
        )
        self.assertEqual(expected, actual)

    def test_inequality(self):
        expected = self.command(
            x=self.x,
            y=self.y,
            z=self.z,
            i=self.i,
            j=self.j,
            f=self.f
        )
        actual = self.command(
            x=self.x,
            y=self.y,
            z=self.z,
            i=self.i,
            j=self.j + 1,
            f=self.f
        )
        self.assertNotEqual(expected, actual)


class TestG3(TestG2):

    def setUp(self, command: type = G2, command_name: str = 'G3'):
        super().setUp(G3, 'G3')


class TestG80(TestCode):

    def test_g80_without_comment(self):
        system_under_test = G80()
        self.assertEqual('G80;', system_under_test.format(self.output_options))

    def test_g80_with_comment(self):
        system_under_test = G80(self.comment)
        self.assertEqual(f'G80; {self.comment}', system_under_test.format(self.output_options))

    def test_equality(self):
        expected = G80(comment=self.comment)
        actual = G80(comment=self.comment)
        self.assertEqual(expected, actual)

    def test_inequality(self):
        expected = G80(comment=self.comment)
        actual = G80(comment=f'not {self.comment}')
        self.assertNotEqual(expected, actual)


class TestG81(TestCode):

    def test_g81_without_comment(self):
        system_under_test = G81(x=self.x, y=self.y, z=self.z, r=self.r, f=self.f)
        self.assertEqual(
            f'G81 {self.x_coord} {self.y_coord} {self.z_coord} {self.r_coord} {self.feed_element};',
            system_under_test.format(self.output_options)
        )

    def test_g81_with_comment(self):
        system_under_test = G81(x=self.x, y=self.y, z=self.z, r=self.r, f=self.f, comment=self.comment)
        self.assertEqual(
            f'G81 {self.x_coord} {self.y_coord} {self.z_coord} {self.r_coord} {self.feed_element}; {self.comment}',
            system_under_test.format(self.output_options)
        )

    def test_g81_without_x(self):
        system_under_test = G81(y=self.y, z=self.z, r=self.r, f=self.f)
        self.assertEqual(
            f'G81 {self.y_coord} {self.z_coord} {self.r_coord} {self.feed_element};',
            system_under_test.format(self.output_options)
        )

    def test_g81_without_y(self):
        system_under_test = G81(x=self.x, z=self.z, r=self.r, f=self.f)
        self.assertEqual(
            f'G81 {self.x_coord} {self.z_coord} {self.r_coord} {self.feed_element};',
            system_under_test.format(self.output_options)
        )

    def test_g81_without_z(self):
        system_under_test = G81(x=self.x, y=self.y, r=self.r, f=self.f)
        self.assertEqual(
            f'G81 {self.x_coord} {self.y_coord} {self.r_coord} {self.feed_element};',
            system_under_test.format(self.output_options)
        )

    def test_equality(self):
        expected = G81(x=self.x, y=self.y, r=self.r, f=self.f)
        actual = G81(x=self.x, y=self.y, r=self.r, f=self.f)
        self.assertEqual(expected, actual)

    def test_inequality(self):
        expected = G81(x=self.x, y=self.y, r=self.r, f=self.f)
        actual = G81(x=self.x, y=self.y, r=self.r + 1, f=self.f)
        self.assertNotEqual(expected, actual)


class TestG82(TestCode):

    def test_g82_without_comment(self):
        system_under_test = G82(x=self.x, y=self.y, z=self.z, r=self.r, p=self.p, f=self.f)
        self.assertEqual(
            f'G82 {self.x_coord} {self.y_coord} {self.z_coord} {self.r_coord} {self.p_time} {self.feed_element};',
            system_under_test.format(self.output_options)
        )

    def test_g82_with_comment(self):
        system_under_test = G82(x=self.x, y=self.y, z=self.z, r=self.r, p=self.p, f=self.f, comment=self.comment)
        self.assertEqual(
            f'G82 {self.x_coord} {self.y_coord} {self.z_coord} {self.r_coord} {self.p_time} {self.feed_element}; {self.comment}',
            system_under_test.format(self.output_options)
        )

    def test_g82_without_x(self):
        system_under_test = G82(y=self.y, z=self.z, r=self.r, p=self.p, f=self.f)
        self.assertEqual(
            f'G82 {self.y_coord} {self.z_coord} {self.r_coord} {self.p_time} {self.feed_element};',
            system_under_test.format(self.output_options)
        )

    def test_g82_without_y(self):
        system_under_test = G82(x=self.x, z=self.z, r=self.r, p=self.p, f=self.f)
        self.assertEqual(
            f'G82 {self.x_coord} {self.z_coord} {self.r_coord} {self.p_time} {self.feed_element};',
            system_under_test.format(self.output_options)
        )

    def test_g82_without_z(self):
        system_under_test = G82(x=self.x, y=self.y, r=self.r, p=self.p, f=self.f)
        self.assertEqual(
            f'G82 {self.x_coord} {self.y_coord} {self.r_coord} {self.p_time} {self.feed_element};',
            system_under_test.format(self.output_options)
        )

    def test_equality(self):
        expected = G82(x=self.x, y=self.y, r=self.r, p=self.p, f=self.f)
        actual = G82(x=self.x, y=self.y, r=self.r, p=self.p, f=self.f)
        self.assertEqual(expected, actual)

    def test_inequality(self):
        expected = G82(x=self.x, y=self.y, r=self.r, p=self.p, f=self.f)
        actual = G82(x=self.x, y=self.y, r=self.r, p=self.p + 1, f=self.f)
        self.assertNotEqual(expected, actual)


class TestG83(TestCode):

    def test_g83_without_comment(self):
        system_under_test = G83(x=self.x, y=self.y, z=self.z, r=self.r, q=self.q, p=self.p, f=self.f)
        self.assertEqual(
            f'G83 {self.x_coord} {self.y_coord} {self.z_coord} {self.r_coord} {self.q_coord} {self.p_time} {self.feed_element};',
            system_under_test.format(self.output_options)
        )

    def test_g83_with_comment(self):
        system_under_test = G83(x=self.x, y=self.y, z=self.z, r=self.r, q=self.q, p=self.p, f=self.f, comment=self.comment)
        self.assertEqual(
            f'G83 {self.x_coord} {self.y_coord} {self.z_coord} {self.r_coord} {self.q_coord} {self.p_time} {self.feed_element}; {self.comment}',
            system_under_test.format(self.output_options)
        )

    def test_g83_without_x(self):
        system_under_test = G83(y=self.y, z=self.z, r=self.r, q=self.q, p=self.p, f=self.f)
        self.assertEqual(
            f'G83 {self.y_coord} {self.z_coord} {self.r_coord} {self.q_coord} {self.p_time} {self.feed_element};',
            system_under_test.format(self.output_options)
        )

    def test_g83_without_y(self):
        system_under_test = G83(x=self.x, z=self.z, r=self.r, q=self.q, p=self.p, f=self.f)
        self.assertEqual(
            f'G83 {self.x_coord} {self.z_coord} {self.r_coord} {self.q_coord} {self.p_time} {self.feed_element};',
            system_under_test.format(self.output_options)
        )

    def test_g83_without_z(self):
        system_under_test = G83(x=self.x, y=self.y, r=self.r, q=self.q, p=self.p, f=self.f)
        self.assertEqual(
            f'G83 {self.x_coord} {self.y_coord} {self.r_coord} {self.q_coord} {self.p_time} {self.feed_element};',
            system_under_test.format(self.output_options)
        )

    def test_g83_without_p(self):
        system_under_test = G83(x=self.x, y=self.y, z=self.z, r=self.r, q=self.q, f=self.f)
        self.assertEqual(
            f'G83 {self.x_coord} {self.y_coord} {self.z_coord} {self.r_coord} {self.q_coord} P0 {self.feed_element};',
            system_under_test.format(self.output_options)
        )

    def test_equality(self):
        expected = G83(x=self.x, y=self.y, z=self.z, r=self.r, q=self.q, f=self.f)
        actual = G83(x=self.x, y=self.y, z=self.z, r=self.r, q=self.q, f=self.f)
        self.assertEqual(expected, actual)

    def test_inequality(self):
        expected = G83(x=self.x, y=self.y, z=self.z, r=self.r, q=self.q, f=self.f)
        actual = G83(x=self.x, y=self.y, z=self.z, r=self.r, q=self.q + 1, f=self.f)
        self.assertNotEqual(expected, actual)


class TestCyclePosition(TestCode):

    def test_cycle_position_without_comment(self):
        system_under_test = CyclePosition(x=self.x, y=self.y, z=self.z)
        self.assertEqual(
            f'{self.x_coord} {self.y_coord} {self.z_coord};',
            system_under_test.format(self.output_options)
        )

    def test_cycle_position_with_comment(self):
        system_under_test = CyclePosition(x=self.x, y=self.y, z=self.z, comment=self.comment)
        self.assertEqual(
            f'{self.x_coord} {self.y_coord} {self.z_coord}; {self.comment}',
            system_under_test.format(self.output_options)
        )

    def test_cycle_position_without_x(self):
        system_under_test = CyclePosition(y=self.y, z=self.z)
        self.assertEqual(
            f'{self.y_coord} {self.z_coord};',
            system_under_test.format(self.output_options)
        )

    def test_cycle_position_without_y(self):
        system_under_test = CyclePosition(x=self.x, z=self.z)
        self.assertEqual(
            f'{self.x_coord} {self.z_coord};',
            system_under_test.format(self.output_options)
        )

    def test_cycle_position_without_z(self):
        system_under_test = CyclePosition(x=self.x, y=self.y)
        self.assertEqual(
            f'{self.x_coord} {self.y_coord};',
            system_under_test.format(self.output_options)
        )

    def test_cycle_position_without_x_or_y(self):
        system_under_test = CyclePosition(z=self.z)
        self.assertEqual(
            f'{self.z_coord};',
            system_under_test.format(self.output_options)
        )

    def test_cycle_position_without_x_or_z(self):
        system_under_test = CyclePosition(y=self.y)
        self.assertEqual(
            f'{self.y_coord};',
            system_under_test.format(self.output_options)
        )

    def test_cycle_position_without_y_or_z(self):
        system_under_test = CyclePosition(x=self.x)
        self.assertEqual(
            f'{self.x_coord};',
            system_under_test.format(self.output_options)
        )

    def test_equality(self):
        expected = CyclePosition(x=self.x, y=self.y, z=self.z)
        actual = CyclePosition(x=self.x, y=self.y, z=self.z)
        self.assertEqual(expected, actual)

    def test_inequality(self):
        expected = CyclePosition(x=self.x, y=self.y, z=self.z)
        actual = CyclePosition(x=self.x, y=self.y, z=self.z + 1)
        self.assertNotEqual(expected, actual)
