from dataclasses import dataclass


@dataclass
class ToolOptions:
    tool_flutes: int
    tool_diameter: float  # mm

    spindle_speed: float  # rpm
    feed_rate: float  # mm per min

    max_stepover: float  # mm
    max_stepdown: float  # mm

    max_helix_stepover: float  # mm
    max_helix_angle: float = 3  # degrees

    finishing_pass: float = 0  # mm
    finishing_feed_rate: float = 0  # mm per min


@dataclass
class JobOptions:
    finishing_climb: bool = True

    clearance_height: float = 10  # mm
    lead_in: float = 0.25  # mm


@dataclass
class OutputOptions:
    position_precision: int = 3  # 10^(-precision) mm
    feed_precision: int = 2  # 10^(-precision) mm
    speed_precision: int = 1  # 10^(-precision) mm


@dataclass
class Options:
    tool: ToolOptions
    job: JobOptions
    output: OutputOptions
