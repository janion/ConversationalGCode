
class ToolOptions:

    def __init__(self,
                 tool_flutes: int,
                 tool_diameter: float,

                 spindle_speed: float,
                 feed_rate: float,

                 max_stepover: float,
                 max_stepdown: float,

                 max_helix_stepover: float,
                 helix_feed_rate: float = None,
                 max_helix_angle: float = 3,

                 corner_feed_rate: float = None,

                 finishing_pass: float = None,
                 finishing_feed_rate: float = None,
                 finishing_climb: bool = True
                 ):
        if helix_feed_rate is None:
            helix_feed_rate = feed_rate
        if corner_feed_rate is None:
            corner_feed_rate = feed_rate
        if finishing_pass is None:
            finishing_pass = 0

        if tool_flutes is None or tool_flutes < 1:
            raise ValueError('Tool flute count must be 1 or more')
        elif tool_diameter is None or tool_diameter <= 0:
            raise ValueError('Tool diameter must be positive')
        elif spindle_speed is None or spindle_speed <= 0:
            raise ValueError('Spindle speed must be positive')
        elif feed_rate is None or feed_rate <= 0:
            raise ValueError('Feed rate must be positive')
        elif max_stepover is None or max_stepover <= 0:
            raise ValueError('Tool step-over must be positive')
        elif max_stepover > tool_diameter:
            raise ValueError('Tool step-over cannot be more than the tool diameter')
        elif max_stepdown is None or max_stepdown <= 0:
            raise ValueError('Tool step-down must be positive')
        elif max_helix_stepover is None or max_helix_stepover <= 0:
            raise ValueError('Helical tool step-over must be positive')
        elif max_helix_stepover > tool_diameter / 2:
            raise ValueError('Helical tool step-over cannot be more than the tool radius')
        elif helix_feed_rate is None or helix_feed_rate <= 0:
            raise ValueError('Helical feed rate must be positive')
        elif max_helix_angle is None or max_helix_angle <= 0 or max_helix_angle >= 90:
            raise ValueError('Helical feed angle must be greater than 0 degrees and less than 90 degrees')
        elif corner_feed_rate <= 0:
            raise ValueError('Corner feed rate must be positive')
        elif finishing_pass < 0:
            raise ValueError('Finishing pass must be positive or None')
        elif finishing_pass > 0 and (finishing_feed_rate is None or finishing_feed_rate <= 0):
            raise ValueError('Finishing feed rate must be positive')
        elif finishing_pass > 0 and finishing_climb is None:
            raise ValueError('Finishing pass must be specified as either climb or conventional cutting direction (True = climb or False = conventional)')

        self._tool_flutes = tool_flutes
        self._tool_diameter = tool_diameter

        self._spindle_speed = spindle_speed
        self._feed_rate = feed_rate

        self._max_stepover = max_stepover
        self._max_stepdown = max_stepdown

        self._max_helix_stepover = max_helix_stepover
        self._helix_feed_rate = helix_feed_rate
        self._max_helix_angle = max_helix_angle

        self._corner_feed_rate = corner_feed_rate

        self._finishing_pass = finishing_pass
        self._finishing_feed_rate = finishing_feed_rate
        self._finishing_climb = finishing_climb

    tool_flutes = property(fget=lambda self: self._tool_flutes)
    tool_diameter = property(fget=lambda self: self._tool_diameter)

    spindle_speed = property(fget=lambda self: self._spindle_speed)
    feed_rate = property(fget=lambda self: self._feed_rate)

    max_stepover = property(fget=lambda self: self._max_stepover)
    max_stepdown = property(fget=lambda self: self._max_stepdown)

    max_helix_stepover = property(fget=lambda self: self._max_helix_stepover)
    helix_feed_rate = property(fget=lambda self: self._helix_feed_rate)
    max_helix_angle = property(fget=lambda self: self._max_helix_angle)

    corner_feed_rate = property(fget=lambda self: self._corner_feed_rate)

    finishing_pass = property(fget=lambda self: self._finishing_pass)
    finishing_feed_rate = property(fget=lambda self: self._finishing_feed_rate)
    finishing_climb = property(fget=lambda self: self._finishing_climb)
