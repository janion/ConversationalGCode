; {
;   "tool": {
;     "tool_flutes": 4,
;     "tool_diameter": 6,
;     "spindle_speed": 1000,
;     "feed_rate": 100,
;     "max_stepover": 2,
;     "max_stepdown": 3,
;     "max_helix_stepover": 2,
;     "max_helix_angle": 3,
;     "finishing_climb": true
;   },
;   "job": {
;     "clearance_height": 10,
;     "lead_in": 0.25
;   },
;   "output": {
;     "position_precision": 3,
;     "feed_precision": 2,
;     "speed_precision": 1
;   }
; }
;
G0 Z10.000; Clear tool
;
M3 S1000.0; Start spindle
;
G0 X0.000 Y0.000; Move to hole position
G0 Z0.250; Move to hole start height
G0 X26.000 Y0.000 Z0.250; Move to hole start position
; Helical interpolation down to step depth
G3 X26.000 Y0.000 Z-2.000 I-26.000 F100.00;
G3 X26.000 Y0.000 Z-2.000 I-26.000 F100.00; Final full pass at depth
; Spiral in to final radius in 2.000mm passes
G3 X-24.000 Y0.000 I-25.000 F100.00;
G3 X24.000 Y0.000 I24.000 F100.00;
G3 X-22.000 Y0.000 I-23.000 F100.00;
G3 X22.000 Y0.000 I22.000 F100.00;
G3 X-20.000 Y0.000 I-21.000 F100.00;
G3 X20.000 Y0.000 I20.000 F100.00;
G3 X-18.000 Y0.000 I-19.000 F100.00;
G3 X18.000 Y0.000 I18.000 F100.00;
G3 X-16.000 Y0.000 I-17.000 F100.00;
G3 X16.000 Y0.000 I16.000 F100.00;
G3 X-16.000 Y0.000 I-16.000 F100.00; Complete circle at final radius
;
G0 X-17.000 Z-1.750; Move cutter away from wall
G0 Z10.000; Clear tool
;
M5; Stop spindle
M2; End program