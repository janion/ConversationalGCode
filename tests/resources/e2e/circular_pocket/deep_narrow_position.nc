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
G0 X12.000 Y13.000; Move to hole position
G0 Z-9.750; Move to hole start depth
G0 X14.000 Y13.000 Z-9.750; Move to hole start position
; Helical interpolation down to step depth
G2 X14.000 Y13.000 Z-10.403 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-11.056 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-11.710 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-12.363 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-13.016 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-13.669 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-14.323 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-14.976 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-15.629 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-16.282 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-16.935 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-17.589 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-18.242 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-18.895 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-19.548 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-20.202 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-20.855 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-21.508 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-22.161 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-22.815 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-23.468 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-24.121 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-24.774 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-25.427 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-26.081 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-26.734 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-27.387 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-28.040 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-28.694 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-29.347 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-30.000 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-30.000 I-2.000 F100.00; Final full pass at depth
G0 X13.000 Z-29.750; Move cutter away from wall
G0 Z10.000; Clear tool
;
M5; Stop spindle
M2; End program