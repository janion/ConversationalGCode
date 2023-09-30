from dataclasses import dataclass


@dataclass
class Comment:
    comment: str = ''

    def format(self, output_options):
        return ';' if self.comment == '' else f'; {self.comment}'

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

    def format(self, output_options):
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
        return f'G2{x_pos}{y_pos}{z_pos}{i_pos}{j_pos}{k_pos}{feed}{end}'

@dataclass
class G3(G2):

    def format(self, output_options):
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
        return f'G3{x_pos}{y_pos}{z_pos}{i_pos}{j_pos}{k_pos}{feed}{end}'
