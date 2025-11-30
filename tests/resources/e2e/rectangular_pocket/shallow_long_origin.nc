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
G0 X0.000 Y-5.000; Move to starting position
G0 Z0.250; Move to hole start depth
; Clear out circle at edge of pocket
G0 X2.000 Y-5.000 Z0.250; Move to hole start position
; Helical interpolation down to step depth
G2 X2.000 Y-5.000 Z-0.312 I-2.000 F100.00;
G2 X2.000 Y-5.000 Z-0.875 I-2.000 F100.00;
G2 X2.000 Y-5.000 Z-1.438 I-2.000 F100.00;
G2 X2.000 Y-5.000 Z-2.000 I-2.000 F100.00;
G2 X2.000 Y-5.000 Z-2.000 I-2.000 F100.00; Final full pass at depth
; Spiral out to final radius in 1.667mm passes
G2 X-3.667 Y-5.000 I-2.833 F100.00;
G2 X3.667 Y-5.000 I3.667 F100.00;
G2 X-5.333 Y-5.000 I-4.500 F100.00;
G2 X5.333 Y-5.000 I5.333 F100.00;
G2 X-7.000 Y-5.000 I-6.167 F100.00;
G2 X7.000 Y-5.000 I7.000 F100.00;
G2 X-7.000 Y-5.000 I-7.000 F100.00; Complete circle at final radius
; Clear nearest corners in 1.450mm passes
; Clear first corner
G0 Z-1.750;
G0 X7.000 Y-5.000;
G0 Z-2.000;
G1 X7.000 Y-9.733 F100.00;
G2 X4.733 Y-12.000 I-7.000 J4.733 F100.00;
G1 X0.000 Y-12.000 F100.00;
G0 Z-1.750;
G0 X7.000 Y-9.733;
G0 Z-2.000;
G1 X7.000 Y-12.000 F100.00;
G1 X4.733 Y-12.000 F100.00;
; Clear second corner
G0 Z-1.750;
G0 X0.000 Y-12.000;
G0 Z-2.000;
G1 X-4.733 Y-12.000 F100.00;
G2 X-7.000 Y-9.733 I4.733 J7.000 F100.00;
G1 X-7.000 Y-5.000 F100.00;
G0 Z-1.750;
G0 X-4.733 Y-12.000;
G0 Z-2.000;
G1 X-7.000 Y-12.000 F100.00;
G1 X-7.000 Y-9.733 F100.00;
; Clear centre in 2.000mm passes
G0 Z-1.750; Move to arc start
G0 X-7.000 Y-5.000;
G0 Z-2.000;
G1 X-7.000 Y0.657 F100.00;
G2 X7.000 Y0.657 I7.000 J-5.657 F100.00;
G1 X7.000 Y-5.000 F100.00;
G0 Z-1.750;
G0 X-7.000 Y0.657;
G0 Z-2.000;
G1 X-7.000 Y3.485 F100.00;
G2 X7.000 Y3.485 I7.000 J-8.485 F100.00;
G1 X7.000 Y0.657 F100.00;
G0 Z-1.750;
G0 X-7.000 Y3.485;
G0 Z-2.000;
G1 X-7.000 Y5.954 F100.00;
G2 X7.000 Y5.954 I7.000 J-10.954 F100.00;
G1 X7.000 Y3.485 F100.00;
G0 Z-1.750;
G0 X-7.000 Y5.954;
G0 Z-2.000;
G1 X-7.000 Y8.266 F100.00;
G2 X7.000 Y8.266 I7.000 J-13.266 F100.00;
G1 X7.000 Y5.954 F100.00;
G0 Z-1.750;
G0 X-7.000 Y8.266;
G0 Z-2.000;
G1 X-7.000 Y10.492 F100.00;
G2 X7.000 Y10.492 I7.000 J-15.492 F100.00;
G1 X7.000 Y8.266 F100.00;
G0 Z-1.750;
G0 X-7.000 Y10.492;
G0 Z-2.000;
; Clear far corners in 1.385mm passes
; First far corner
G1 X-7.000 Y12.000 F100.00;
G1 X0.000 Y12.000 F100.00;
; Second far corner
G0 Z-1.750; Move to arc start
G0 X0.000 Y12.000;
G0 Z-2.000;
G1 X7.000 Y12.000 F100.00;
G1 X7.000 Y10.492 F100.00;
G0 X6.000 Y9.492 Z-1.750; Clear wall
G0 Z10.000; Clear tool
;
M5; Stop spindle
M2; End program