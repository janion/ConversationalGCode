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
G0 X-5.000 Y0.000; Move to starting position
G0 Z0.250; Move to hole start depth
; Clear out circle at edge of pocket
G0 X-5.000 Y-2.000 Z0.250; Move to hole start position
; Helical interpolation down to step depth
G2 X-5.000 Y-2.000 Z-0.312 J2.000 F100.00;
G2 X-5.000 Y-2.000 Z-0.875 J2.000 F100.00;
G2 X-5.000 Y-2.000 Z-1.438 J2.000 F100.00;
G2 X-5.000 Y-2.000 Z-2.000 J2.000 F100.00;
G2 X-5.000 Y-2.000 Z-2.000 J2.000 F100.00; Final full pass at depth
; Spiral out to final radius in 1.667mm passes
G2 X-5.000 Y3.667 J2.833 F100.00;
G2 X-5.000 Y-3.667 J-3.667 F100.00;
G2 X-5.000 Y5.333 J4.500 F100.00;
G2 X-5.000 Y-5.333 J-5.333 F100.00;
G2 X-5.000 Y7.000 J6.167 F100.00;
G2 X-5.000 Y-7.000 J-7.000 F100.00;
G2 X-5.000 Y7.000 J7.000 F100.00; Complete circle at final radius
; Clear nearest corners in 1.450mm passes
; Clear first corner
G0 Z-1.750;
G0 X-5.000 Y-7.000;
G0 Z-2.000;
G1 X-9.733 Y-7.000 F100.00;
G2 X-12.000 Y-4.733 I4.733 J7.000 F100.00;
G1 X-12.000 Y0.000 F100.00;
G0 Z-1.750;
G0 X-9.733 Y-7.000;
G0 Z-2.000;
G1 X-12.000 Y-7.000 F100.00;
G1 X-12.000 Y-4.733 F100.00;
; Clear second corner
G0 Z-1.750;
G0 X-12.000 Y0.000;
G0 Z-2.000;
G1 X-12.000 Y4.733 F100.00;
G2 X-9.733 Y7.000 I7.000 J-4.733 F100.00;
G1 X-5.000 Y7.000 F100.00;
G0 Z-1.750;
G0 X-12.000 Y4.733;
G0 Z-2.000;
G1 X-12.000 Y7.000 F100.00;
G1 X-9.733 Y7.000 F100.00;
; Clear centre in 2.000mm passes
G0 Z-1.750; Move to arc start
G0 X-5.000 Y7.000;
G0 Z-2.000;
G1 X0.657 Y7.000 F100.00;
G2 X0.657 Y-7.000 I-5.657 J-7.000 F100.00;
G1 X-5.000 Y-7.000 F100.00;
G0 Z-1.750;
G0 X0.657 Y7.000;
G0 Z-2.000;
G1 X3.485 Y7.000 F100.00;
G2 X3.485 Y-7.000 I-8.485 J-7.000 F100.00;
G1 X0.657 Y-7.000 F100.00;
G0 Z-1.750;
G0 X3.485 Y7.000;
G0 Z-2.000;
G1 X5.954 Y7.000 F100.00;
G2 X5.954 Y-7.000 I-10.954 J-7.000 F100.00;
G1 X3.485 Y-7.000 F100.00;
G0 Z-1.750;
G0 X5.954 Y7.000;
G0 Z-2.000;
G1 X8.266 Y7.000 F100.00;
G2 X8.266 Y-7.000 I-13.266 J-7.000 F100.00;
G1 X5.954 Y-7.000 F100.00;
G0 Z-1.750;
G0 X8.266 Y7.000;
G0 Z-2.000;
G1 X10.492 Y7.000 F100.00;
G2 X10.492 Y-7.000 I-15.492 J-7.000 F100.00;
G1 X8.266 Y-7.000 F100.00;
G0 Z-1.750;
G0 X10.492 Y7.000;
G0 Z-2.000;
; Clear far corners in 1.385mm passes
; First far corner
G1 X12.000 Y7.000 F100.00;
G1 X12.000 Y0.000 F100.00;
; Second far corner
G0 Z-1.750; Move to arc start
G0 X12.000 Y0.000;
G0 Z-2.000;
G1 X12.000 Y-7.000 F100.00;
G1 X10.492 Y-7.000 F100.00;
G0 X9.492 Y-6.000 Z-1.750; Clear wall
G0 Z10.000; Clear tool
;
M5; Stop spindle
M2; End program