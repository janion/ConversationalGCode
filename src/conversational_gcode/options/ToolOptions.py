from conversational_gcode.validate.validation_result import ValidationResult


class ToolOptions:

    def __init__(self,
                 tool_flutes: int = 4,
                 tool_diameter: float = 6,

                 spindle_speed: float = 1000,
                 feed_rate: float = 100,

                 max_stepover: float = 2,
                 max_stepdown: float = 3,

                 max_helix_stepover: float = 2,
                 helix_feed_rate: float = None,
                 max_helix_angle: float = 3,

                 finishing_pass: float = None,
                 finishing_feed_rate: float = None,
                 finishing_climb: bool = True
                 ):
        self._tool_flutes = tool_flutes
        self._tool_diameter = tool_diameter

        self._spindle_speed = spindle_speed
        self._feed_rate = feed_rate

        self._max_stepover = max_stepover
        self._max_stepdown = max_stepdown

        self._max_helix_stepover = max_helix_stepover
        self._helix_feed_rate = helix_feed_rate
        self._max_helix_angle = max_helix_angle

        self._finishing_pass = finishing_pass
        self._finishing_feed_rate = finishing_feed_rate
        self._finishing_climb = finishing_climb

    def validate(self):
        results = []
        if self._tool_flutes is None or self._tool_flutes < 1:
            results.append(ValidationResult(False, 'Tool flute count must be 1 or more'))
        if self._tool_diameter is None or self._tool_diameter <= 0:
            results.append(ValidationResult(False, 'Tool diameter must be positive'))
        if self._spindle_speed is None or self._spindle_speed <= 0:
            results.append(ValidationResult(False, 'Spindle speed must be positive'))
        if self._feed_rate is None or self._feed_rate <= 0:
            results.append(ValidationResult(False, 'Feed rate must be positive'))
        if self._max_stepover is None or self._max_stepover <= 0:
            results.append(ValidationResult(False, 'Tool step-over must be positive'))
        if self._max_stepover > self._tool_diameter:
            results.append(ValidationResult(False, 'Tool step-over cannot be more than the tool diameter'))
        if self._max_stepdown is None or self._max_stepdown <= 0:
            results.append(ValidationResult(False, 'Tool step-down must be positive'))
        if self._max_helix_stepover is None or self._max_helix_stepover <= 0:
            results.append(ValidationResult(False, 'Helical tool step-over must be positive'))
        if self._max_helix_stepover > self._tool_diameter / 2:
            results.append(ValidationResult(False, 'Helical tool step-over cannot be more than the tool radius'))
        if self._helix_feed_rate is None or self._helix_feed_rate <= 0:
            results.append(ValidationResult(False, 'Helical feed rate must be positive'))
        if self._max_helix_angle is None or self._max_helix_angle <= 0 or self._max_helix_angle >= 90:
            results.append(ValidationResult(False, 'Helical feed angle must be greater than 0 degrees and less than 90 degrees'))
        if self._finishing_pass is not None:
            if self._finishing_pass < 0:
                results.append(ValidationResult(False, 'Finishing pass must be positive or None'))
            if self._finishing_pass > 0 and (self._finishing_feed_rate is None or self._finishing_feed_rate <= 0):
                results.append(ValidationResult(False, 'Finishing feed rate must be positive'))
            if self._finishing_pass > 0 and self._finishing_climb is None:
                results.append(ValidationResult(False, 'Finishing pass must be specified as either climb or conventional cutting direction (True = climb or False = conventional)'))
            
        if len(results) == 0:
            results.append(ValidationResult())
        
        return results

    def _set_tool_flutes(self, value):
        self._tool_flutes = value

    def _set_tool_diameter(self, value):
        self._tool_diameter = value

    def _set_spindle_speed(self, value):
        self._spindle_speed = value

    def _set_feed_rate(self, value):
        self._feed_rate = value

    def _set_max_stepover(self, value):
        self._max_stepover = value

    def _set_max_stepdown(self, value):
        self._max_stepdown = value

    def _set_max_helix_stepover(self, value):
        self._max_helix_stepover = value

    def _set_helix_feed_rate(self, value):
        self._helix_feed_rate = value

    def _set_max_helix_angle(self, value):
        self._max_helix_angle = value

    def _set_finishing_pass(self, value):
        self._finishing_pass = value

    def _set_finishing_feed_rate(self, value):
        self._finishing_feed_rate = value

    def _set_finishing_climb(self, value):
        self._finishing_climb = value

    tool_flutes = property(
        fget=lambda self: self._tool_flutes,
        fset=_set_tool_flutes
    )
    tool_diameter = property(
        fget=lambda self: self._tool_diameter,
        fset=_set_tool_diameter
    )

    spindle_speed = property(
        fget=lambda self: self._spindle_speed,
        fset=_set_spindle_speed
    )
    feed_rate = property(
        fget=lambda self: self._feed_rate,
        fset=_set_feed_rate
    )

    max_stepover = property(
        fget=lambda self: self._max_stepover,
        fset=_set_max_stepover
    )
    max_stepdown = property(
        fget=lambda self: self._max_stepdown,
        fset=_set_max_stepdown
    )

    max_helix_stepover = property(
        fget=lambda self: self._max_helix_stepover,
        fset=_set_max_helix_stepover
    )
    helix_feed_rate = property(
        fget=lambda self: self._helix_feed_rate,
        fset=_set_helix_feed_rate
    )
    max_helix_angle = property(
        fget=lambda self: self._max_helix_angle,
        fset=_set_max_helix_angle
    )

    finishing_pass = property(
        fget=lambda self: self._finishing_pass if self._finishing_pass is not None else 0,
        fset=_set_finishing_pass
    )
    finishing_feed_rate = property(
        fget=lambda self: self._finishing_feed_rate if self._finishing_feed_rate is not None else self._feed_rate,
        fset=_set_finishing_feed_rate
    )
    finishing_climb = property(
        fget=lambda self: self._finishing_climb,
        fset=_set_finishing_climb
    )
