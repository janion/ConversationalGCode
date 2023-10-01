from dataclasses import dataclass


@dataclass
class Comment:
    comment: str = ''

    def format(self, output_options):
        return ';' if self.comment == '' else f'; {self.comment}'

    def transform(self, transformation):
        return self


@dataclass
class M2(Comment):

    def format(self, output_options):
        end = ';' if self.comment == '' else f'; {self.comment}'
        return f'M2{end}'


@dataclass
class M3(Comment):
    s: float = None  # rpm

    def format(self, output_options):
        speed_precision = output_options.speed_precision
        rpm = f' S{self.s:.{speed_precision}f}'
        end = ';' if self.comment == '' else f'; {self.comment}'
        return f'M3{rpm}{end}'


@dataclass
class M5(Comment):

    def format(self, output_options):
        end = ';' if self.comment == '' else f'; {self.comment}'
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
        end = ';' if self.comment == '' else f'; {self.comment}'
        return f'G0{x_pos}{y_pos}{z_pos}{end}'

    def transform(self, transformation):
        new_x = transformation.absolute[0](self.x, self.y)
        new_y = transformation.absolute[1](self.x, self.y)
        self.x = new_x
        self.y = new_y

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
        end = ';' if self.comment == '' else f'; {self.comment}'
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
        end = ';' if self.comment == '' else f'; {self.comment}'
        return f'{command}{x_pos}{y_pos}{z_pos}{i_pos}{j_pos}{k_pos}{feed}{end}'

    def format(self, output_options):
        return self._format_arc('G2', output_options)

    def transform(self, transformation):
        super().transform(transformation)

        new_i = transformation.relative[0](self.i, self.j)
        new_j = transformation.relative[1](self.i, self.j)

        self.i = new_i
        self.j = new_j

        return self


@dataclass
class G3(G2):

    def format(self, output_options):
        return self._format_arc('G3', output_options)
