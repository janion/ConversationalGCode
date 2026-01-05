"""
GCode command objects which are exported by the various operations.

Classes:
- GCode
  - Prints a line, starting with a semicolon, with text comment following it.
- M2
  - Prints an M2 command to stop the machine spindle.
- M3
  - Prints an M3 command to start the machine spindle.
- M5
  - Prints an M5 command to end the program.
- G0
  - Prints a G0 command to rapidly move the tool to a given location.
- G1
  - Prints a G1 command to feed the tool to a given location.
- G2
  - Prints a G2 command to feed the tool in a clockwise circular arc.
- G3
  - Prints a G3 command to feed the tool in an anticlockwise circular arc.
- G80
  - Prints a G80 command to end a canned cycle.
- G81
  - Prints a G81 command to start a canned cycle for drilling.
- G82
  - Prints a G82 command to start a canned cycle for spot drilling.
- G83
  - Prints a G81 command to start a canned cycle for peck drilling.
- CyclePosition
  - Prints an XY location for use within a canned cycle.
"""

from conversational_gcode.options.OutputOptions import OutputOptions
from conversational_gcode.position.Position import Position
from conversational_gcode.transform.Transformation import Transformation

from dataclasses import dataclass
from typing import Self


@dataclass
class GCode:
    """
    An empty line with a comment in a GCode file.

    Attributes:
        comment (str): An optional comment to print at the end of the line.
    """
    comment: str = None

    def format(self, output_options: OutputOptions) -> str:
        return ';' if self.comment is None else f'; {self.comment}'

    def transform(self, transformation: Transformation) -> Self:
        return self

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, GCode):
            return False

        return self.comment == __o.comment

    def __repr__(self) -> str:
        return f'GCode(comment={self.comment})'


@dataclass
class M2(GCode):
    """
    An M2 command to stop the machine spindle.

    Attributes:
        comment (str): An optional comment to print at the end of the line.
    """

    def format(self, output_options: OutputOptions) -> str:
        end = ';' if self.comment is None else f'; {self.comment}'
        return f'M2{end}'

    def __eq__(self, __o: object) -> bool:
        if not super().__eq__(__o):
            return False

        return isinstance(__o, M2)

    def __repr__(self) -> str:
        return f'M2(comment={self.comment})'


@dataclass
class M3(GCode):
    """
    An M3 command to start the machine spindle.

    Attributes:
        s (float): The RPM (revolutions per minute) at which to set the spindle.
        comment (str): An optional comment to print at the end of the line.
    """
    s: float = None  # rpm

    def format(self, output_options: OutputOptions) -> str:
        speed_precision = output_options.speed_precision
        rpm = f' S{self.s:.{speed_precision}f}'
        end = ';' if self.comment is None else f'; {self.comment}'
        return f'M3{rpm}{end}'

    def __eq__(self, __o: object) -> bool:
        if not super().__eq__(__o):
            return False

        if not isinstance(__o, M3):
            return False

        return self.s == __o.s

    def __repr__(self) -> str:
        return f'M3(s={self.s}, comment={self.comment})'


@dataclass
class M5(GCode):
    """
    An M2 command to end the GCode program.

    Attributes:
        comment (str): An optional comment to print at the end of the line.
    """

    def format(self, output_options: OutputOptions) -> str:
        end = ';' if self.comment is None else f'; {self.comment}'
        return f'M5{end}'

    def __eq__(self, __o: object) -> bool:
        if not super().__eq__(__o):
            return False

        return isinstance(__o, M5)

    def __repr__(self) -> str:
        return f'M5(comment={self.comment})'


@dataclass
class G0(GCode):
    """
    G0 command to rapidly move the tool to a given location.

    Attributes:
        x (float): The X-axis location to which to move the tool.
        y (float): The Y-axis location to which to move the tool.
        z (float): The Z-axis location to which to move the tool.
        comment (str): An optional comment to print at the end of the line.
    """

    x: float = None  # mm
    y: float = None  # mm
    z: float = None  # mm

    def format(self, output_options: OutputOptions) -> str:
        position_precision = output_options.position_precision
        x_pos = f' X{self.x:.{position_precision}f}' if self.x is not None else ''
        y_pos = f' Y{self.y:.{position_precision}f}' if self.y is not None else ''
        z_pos = f' Z{self.z:.{position_precision}f}' if self.z is not None else ''
        end = ';' if self.comment is None else f'; {self.comment}'
        return f'G0{x_pos}{y_pos}{z_pos}{end}'

    def transform(self, transformation: Transformation) -> Self:
        new_point = transformation.transform_absolute(Position(self.x, self.y, self.z))
        self.x = new_point.x
        self.y = new_point.y
        self.z = new_point.z

        return self

    def __eq__(self, __o: object) -> bool:
        if not super().__eq__(__o):
            return False

        if not isinstance(__o, G0):
            return False

        return (self.x == __o.x and
                self.y == __o.y and
                self.z == __o.z)

    def __repr__(self) -> str:
        return f'G0(x={self.x}, y={self.y}, z={self.z}, comment={self.comment})'


@dataclass
class G1(G0):
    """
    G1 command to feed the tool to a given location.

    Attributes:
        x (float): The X-axis location to which to move the tool.
        y (float): The Y-axis location to which to move the tool.
        z (float): The Z-axis location to which to move the tool.
        f (float): The feed rate at which to move the tool.
        comment (str): An optional comment to print at the end of the line.
    """
    f: float = None  # mm per min

    def format(self, output_options: OutputOptions) -> str:
        position_precision = output_options.position_precision
        feed_precision = output_options.feed_precision
        x_pos = f' X{self.x:.{position_precision}f}' if self.x is not None else ''
        y_pos = f' Y{self.y:.{position_precision}f}' if self.y is not None else ''
        z_pos = f' Z{self.z:.{position_precision}f}' if self.z is not None else ''
        feed = f' F{self.f:.{feed_precision}f}'
        end = ';' if self.comment is None else f'; {self.comment}'
        return f'G1{x_pos}{y_pos}{z_pos}{feed}{end}'

    def __eq__(self, __o: object) -> bool:
        if not super().__eq__(__o):
            return False

        if not isinstance(__o, G1):
            return False

        return self.f == __o.f

    def __repr__(self) -> str:
        return f'G1(x={self.x}, y={self.y}, z={self.z}, f={self.f}, comment={self.comment})'


@dataclass
class G2(G1):
    """
    G2 command to feed the tool to a given location via a clockwise circular arc.

    Attributes:
        x (float): The X-axis location to which to move the tool.
        y (float): The Y-axis location to which to move the tool.
        z (float): The Z-axis location to which to move the tool.
        i (float): The relative X-axis location of the arc centre about which to move the tool.
            This is relative to the starting location.
        j (float): The relative Y-axis location of the arc centre about which to move the tool.
            This is relative to the starting location.
        k (float): The relative Z-axis location of the arc centre about which to move the tool.
            This is relative to the starting location.
        f (float): The feed rate at which to move the tool.
        comment (str): An optional comment to print at the end of the line.
    """
    i: float = None  # mm
    j: float = None  # mm
    k: float = None  # mm

    def _format_arc(self, command, output_options):
        position_precision = output_options.position_precision
        feed_precision = output_options.feed_precision
        x_pos = f' X{self.x:.{position_precision}f}' if self.x is not None else ''
        y_pos = f' Y{self.y:.{position_precision}f}' if self.y is not None else ''
        z_pos = f' Z{self.z:.{position_precision}f}' if self.z is not None else ''
        i_pos = f' I{self.i:.{position_precision}f}' if self.i is not None else ''
        j_pos = f' J{self.j:.{position_precision}f}' if self.j is not None else ''
        k_pos = f' K{self.k:.{position_precision}f}' if self.k is not None else ''
        feed = f' F{self.f:.{feed_precision}f}'
        end = ';' if self.comment is None else f'; {self.comment}'
        return f'{command}{x_pos}{y_pos}{z_pos}{i_pos}{j_pos}{k_pos}{feed}{end}'

    def format(self, output_options: OutputOptions) -> str:
        return self._format_arc('G2', output_options)

    def transform(self, transformation: Transformation) -> Self:
        super().transform(transformation)

        new_point = transformation.transform_relative(Position(self.i, self.j, self.k))

        self.i = new_point.x
        self.j = new_point.y
        self.k = new_point.z

        return self

    def __eq__(self, __o: object) -> bool:
        if not super().__eq__(__o):
            return False

        if not isinstance(__o, G2):
            return False

        return (self.i == __o.i and
                self.j == __o.j and
                self.k == __o.k)

    def __repr__(self) -> str:
        return (
            'G2(' +
            f'x={self.x}, y={self.y}, z={self.z}, '+
            f'i={self.i}, j={self.j}, k={self.k}, ' +
            f'f={self.f}, comment={self.comment}' +
            ')'
        )


@dataclass
class G3(G2):
    """
    G3 command to feed the tool to a given location via an anticlockwise circular arc.

    Attributes:
        x (float): The X-axis location to which to move the tool.
        y (float): The Y-axis location to which to move the tool.
        z (float): The Z-axis location to which to move the tool.
        i (float): The relative X-axis location of the arc centre about which to move the tool.
            This is relative to the starting location.
        j (float): The relative Y-axis location of the arc centre about which to move the tool.
            This is relative to the starting location.
        k (float): The relative Z-axis location of the arc centre about which to move the tool.
            This is relative to the starting location.
        f (float): The feed rate at which to move the tool.
        comment (str): An optional comment to print at the end of the line.
    """

    def format(self, output_options: OutputOptions) -> str:
        return self._format_arc('G3', output_options)

    def __eq__(self, __o: object) -> bool:
        if not super().__eq__(__o):
            return False

        return isinstance(__o, G3)

    def __repr__(self) -> str:
        return (
            'G3(' +
            f'x={self.x}, y={self.y}, z={self.z}, '+
            f'i={self.i}, j={self.j}, k={self.k}, ' +
            f'f={self.f}, comment={self.comment}' +
            ')'
        )


class G80(GCode):
    """
    G80 command to finish a canned cycle.

    Attributes:
        comment (str): An optional comment to print at the end of the line.
    """

    def format(self, output_options: OutputOptions) -> str:
        end = ';' if self.comment is None else f'; {self.comment}'
        return f'G80{end}'

    def __eq__(self, __o: object) -> bool:
        if not super().__eq__(__o):
            return False

        return isinstance(__o, G80)

    def __repr__(self) -> str:
        return f'G80(comment={self.comment})'


@dataclass
class G81(G1):
    """
    G81 command to feed the tool to start a canned cycle for drilling.

    Attributes:
        x (float): The X-axis location to which to drill the first hole.
        y (float): The Y-axis location to which to drill the first hole.
        z (float): The Z-axis depth of the holes.
        r (float): The retraction height to pull back to between holes.
        f (float): The feed rate at which to advance the drill.
        comment (str): An optional comment to print at the end of the line.
    """
    r: float = None  # mm

    def format(self, output_options: OutputOptions) -> str:
        position_precision = output_options.position_precision
        feed_precision = output_options.feed_precision
        x_pos = f' X{self.x:.{position_precision}f}' if self.x is not None else ''
        y_pos = f' Y{self.y:.{position_precision}f}' if self.y is not None else ''
        z_pos = f' Z{self.z:.{position_precision}f}' if self.z is not None else ''
        r = f' R{self.r:.{position_precision}f}'
        feed = f' F{self.f:.{feed_precision}f}'
        end = ';' if self.comment is None else f'; {self.comment}'
        return f'G81{x_pos}{y_pos}{z_pos}{r}{feed}{end}'

    def __eq__(self, __o: object) -> bool:
        if not super().__eq__(__o):
            return False

        if not isinstance(__o, G81):
            return False

        return self.r == __o.r

    def __repr__(self) -> str:
        return f'G81(x={self.x}, y={self.y}, z={self.z}, r={self.r}, f={self.f}, comment={self.comment})'


@dataclass
class G82(G81):
    """
    G82 command to feed the tool to start a canned cycle for spot drilling.

    Attributes:
        x (float): The X-axis location to which to drill the first hole.
        y (float): The Y-axis location to which to drill the first hole.
        z (float): The Z-axis depth of the holes.
        r (float): The retraction height to pull back to between holes.
        p (int): The dwell time at the bottom of the hole, in milliseconds.
        f (float): The feed rate at which to advance the drill.
        comment (str): An optional comment to print at the end of the line.
    """
    p: int = None  # ms

    def format(self, output_options: OutputOptions) -> str:
        position_precision = output_options.position_precision
        feed_precision = output_options.feed_precision
        x_pos = f' X{self.x:.{position_precision}f}' if self.x is not None else ''
        y_pos = f' Y{self.y:.{position_precision}f}' if self.y is not None else ''
        z_pos = f' Z{self.z:.{position_precision}f}' if self.z is not None else ''
        r = f' R{self.r:.{position_precision}f}'
        p = f' P{self.p:d}'
        feed = f' F{self.f:.{feed_precision}f}'
        end = ';' if self.comment is None else f'; {self.comment}'
        return f'G82{x_pos}{y_pos}{z_pos}{r}{p}{feed}{end}'

    def __eq__(self, __o: object) -> bool:
        if not super().__eq__(__o):
            return False

        if not isinstance(__o, G82):
            return False

        return self.p == __o.p

    def __repr__(self) -> str:
        return f'G82(x={self.x}, y={self.y}, z={self.z}, r={self.r}, p={self.p}, f={self.f}, comment={self.comment})'


@dataclass
class G83(G82):
    """
    G83 command to feed the tool to start a canned cycle for peck drilling.

    Attributes:
        x (float): The X-axis location to which to drill the first hole.
        y (float): The Y-axis location to which to drill the first hole.
        z (float): The Z-axis depth of the holes.
        r (float): The retraction height to pull back to between holes.
        q (float): The distance at which a peck retraction should be performed.
        p (float): The dwell time at the bottom of the hole, in milliseconds. Optional.
        f (float): The feed rate at which to advance the drill.
        comment (str): An optional comment to print at the end of the line.
    """
    q: float = None  # mm

    def format(self, output_options: OutputOptions) -> str:
        position_precision = output_options.position_precision
        feed_precision = output_options.feed_precision
        x_pos = f' X{self.x:.{position_precision}f}' if self.x is not None else ''
        y_pos = f' Y{self.y:.{position_precision}f}' if self.y is not None else ''
        z_pos = f' Z{self.z:.{position_precision}f}' if self.z is not None else ''
        r = f' R{self.r:.{position_precision}f}'
        q = f' Q{self.q:.{position_precision}f}'
        p = f' P{self.p:d}' if self.p is not None else ' P0'
        feed = f' F{self.f:.{feed_precision}f}'
        end = ';' if self.comment is None else f'; {self.comment}'
        return f'G83{x_pos}{y_pos}{z_pos}{r}{q}{p}{feed}{end}'

    def __eq__(self, __o: object) -> bool:
        if not super().__eq__(__o):
            return False

        if not isinstance(__o, G83):
            return False

        return self.q == __o.q

    def __repr__(self) -> str:
        return (
            'G83(' +
            f'x={self.x}, y={self.y}, z={self.z}, ' +
            f'r={self.r}, p={self.p}, q={self.q}, ' +
            f'f={self.f}, comment={self.comment}' +
            ')'
        )


@dataclass
class CyclePosition(G0):
    """
    A command for a position in a canned cycle.

    Attributes:
        x (float): The X-axis location at which to drill.
        y (float): The Y-axis location at which to drill.
        z (float): The Z-axis location at which to drill.
        comment (str): An optional comment to print at the end of the line.
    """

    def format(self, output_options: OutputOptions) -> str:
        position_precision = output_options.position_precision
        x_pos = f'X{self.x:.{position_precision}f}' if self.x is not None else ''

        spacer_xy = ' ' if x_pos != '' and self.y is not None else ''
        y_pos = f'Y{self.y:.{position_precision}f}' if self.y is not None else ''

        spacer_yz = ' ' if (y_pos != '' or x_pos != '') and self.z is not None else ''
        z_pos = f'Z{self.z:.{position_precision}f}' if self.z is not None else ''

        end = ';' if self.comment is None else f'; {self.comment}'
        return f'{x_pos}{spacer_xy}{y_pos}{spacer_yz}{z_pos}{end}'

    def __eq__(self, __o: object) -> bool:
        if not super().__eq__(__o):
            return False

        return isinstance(__o, CyclePosition)

    def __repr__(self) -> str:
        return f'CyclePosition(x={self.x}, y={self.y}, z={self.z}, comment={self.comment})'
