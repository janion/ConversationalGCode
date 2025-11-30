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
G0 Z0.250; Move to hole start depth
G0 X2.000 Y0.000 Z0.250; Move to hole start position
; Helical interpolation down to step depth
G2 X2.000 Y0.000 Z-0.312 I-2.000 F100.00;
G2 X2.000 Y0.000 Z-0.875 I-2.000 F100.00;
G2 X2.000 Y0.000 Z-1.438 I-2.000 F100.00;
G2 X2.000 Y0.000 Z-2.000 I-2.000 F100.00;
G2 X2.000 Y0.000 Z-2.000 I-2.000 F100.00; Final full pass at depth
; Spiral out to final radius in 2.000mm passes
G2 X-4.000 Y0.000 I-3.000 F100.00;
G2 X4.000 Y0.000 I4.000 F100.00;
G2 X-6.000 Y0.000 I-5.000 F100.00;
G2 X6.000 Y0.000 I6.000 F100.00;
G2 X-8.000 Y0.000 I-7.000 F100.00;
G2 X8.000 Y0.000 I8.000 F100.00;
G2 X-10.000 Y0.000 I-9.000 F100.00;
G2 X10.000 Y0.000 I10.000 F100.00;
G2 X-10.000 Y0.000 I-10.000 F100.00; Complete circle at final radius
;
G0 X-9.000 Z-1.750; Move cutter away from wall
G0 Z10.000; Clear tool
;
M5; Stop spindle
M2; End program