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
G0 X12.000 Y7.000; Move to starting position
G0 Z0.250; Move to start depth
G1 X12.000 Y-7.000 Z-0.164 F100.00;
G1 X-12.000 Y-7.000 Z-0.875 F100.00;
G1 X-12.000 Y7.000 Z-1.289 F100.00;
G1 X12.000 Y7.000 Z-2.000 F100.00;
; Final pass at full depth
G1 X12.000 Y-7.000 F100.00;
G1 X-12.000 Y-7.000 F100.00;
G1 X-12.000 Y7.000 F100.00;
G1 X12.000 Y7.000 F100.00;
G0 Z10.000; Clear tool
;
M5; Stop spindle
M2; End program