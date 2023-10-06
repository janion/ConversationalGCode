from dataclasses import dataclass


@dataclass
class Comment:
    comment: str = None

    def format(self, output_options):
        return ';' if self.comment is None else f'; {self.comment}'

    def transform(self, transformation):
        return self


@dataclass
class M2(Comment):

    def format(self, output_options):
        end = ';' if self.comment is None else f'; {self.comment}'
        return f'M2{end}'


@dataclass
class M3(Comment):
    s: float = None  # rpm

    def format(self, output_options):
        speed_precision = output_options.speed_precision
        rpm = f' S{self.s:.{speed_precision}f}'
        end = ';' if self.comment is None else f'; {self.comment}'
        return f'M3{rpm}{end}'


@dataclass
class M5(Comment):

    def format(self, output_options):
        end = ';' if self.comment is None else f'; {self.comment}'
        return f'M5{end}'


@dataclass
class G0(Comment):
    x: float = None  # mm
    y: float = None  # mm
    z: float = None  # mm

    def format(self, output_options):
        position_precision = output_options.position_precision
        x_pos = f' X{self.x:.{position_precision}f}' if self.x is not None else ''
        y_pos = f' Y{self.y:.{position_precision}f}' if self.y is not None else ''
        z_pos = f' Z{self.z:.{position_precision}f}' if self.z is not None else ''
        end = ';' if self.comment is None else f'; {self.comment}'
        return f'G0{x_pos}{y_pos}{z_pos}{end}'

    def transform(self, transformation):
        new_point = transformation.transform_absolute([self.x, self.y, self.z])
        self.x = new_point[0]
        self.y = new_point[1]
        self.z = new_point[2]

        return self


@dataclass
class G1(G0):
    f: float = None  # mm per min

    def format(self, output_options):
        position_precision = output_options.position_precision
        feed_precision = output_options.feed_precision
        x_pos = f' X{self.x:.{position_precision}f}' if self.x is not None else ''
        y_pos = f' Y{self.y:.{position_precision}f}' if self.y is not None else ''
        z_pos = f' Z{self.z:.{position_precision}f}' if self.z is not None else ''
        feed = f' F{self.f:.{feed_precision}f}'
        end = ';' if self.comment is None else f'; {self.comment}'
        return f'G1{x_pos}{y_pos}{z_pos}{feed}{end}'


@dataclass
class G2(G1):
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

    def format(self, output_options):
        return self._format_arc('G2', output_options)

    def transform(self, transformation):
        super().transform(transformation)

        new_point = transformation.transform_relative([self.i, self.j, self.k])

        self.i = new_point[0]
        self.j = new_point[1]
        self.k = new_point[2]

        return self


@dataclass
class G3(G2):

    def format(self, output_options):
        return self._format_arc('G3', output_options)


class G80(Comment):

    def format(self, output_options):
        end = ';' if self.comment is None else f'; {self.comment}'
        return f'G80{end}'


@dataclass
class G81(Comment):
    z: float = None  # mm
    r: float = None  # mm
    f: float = None  # mm per min

    def format(self, output_options):
        position_precision = output_options.position_precision
        feed_precision = output_options.feed_precision
        z_pos = f' Z{self.z:.{position_precision}f}'
        r = f' R{self.r:.{position_precision}f}'
        feed = f' F{self.f:.{feed_precision}f}'
        end = ';' if self.comment is None else f'; {self.comment}'
        return f'G81{z_pos}{r}{feed}{end}'


@dataclass
class G82(G81):
    p: float = 0  # ms

    def format(self, output_options):
        position_precision = output_options.position_precision
        feed_precision = output_options.feed_precision
        z_pos = f' Z{self.z:.{position_precision}f}'
        r = f' R{self.r:.{position_precision}f}'
        p = f' P{self.p:.{position_precision}f}'
        feed = f' F{self.f:.{feed_precision}f}'
        end = ';' if self.comment is None else f'; {self.comment}'
        return f'G82{z_pos}{r}{p}{feed}{end}'


@dataclass
class G83(G81):
    i: float = None  # mm

    def format(self, output_options):
        position_precision = output_options.position_precision
        feed_precision = output_options.feed_precision
        z_pos = f' Z{self.z:.{position_precision}f}'
        r = f' R{self.r:.{position_precision}f}'
        i = f' I{self.i:.{position_precision}f}'
        feed = f' F{self.f:.{feed_precision}f}'
        end = ';' if self.comment is None else f'; {self.comment}'
        return f'G82{z_pos}{r}{i}{feed}{end}'


@dataclass
class CyclePosition(Comment):
    x: float = None  # mm
    y: float = None  # mm

    def format(self, output_options):
        position_precision = output_options.position_precision
        x_pos = f'X{self.x:.{position_precision}f}' if self.x is not None else ''
        spacer = ' ' if x_pos != '' else ''
        y_pos = f'Y{self.y:.{position_precision}f}' if self.y is not None else ''
        end = ';' if self.comment is None else f'; {self.comment}'
        return f'{x_pos}{spacer}{y_pos}{end}'
