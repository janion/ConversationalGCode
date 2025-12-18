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
G0 Z-9.750; Move to hole start height
G0 X20.000 Y13.000 Z-9.750; Move to hole start position
; Helical interpolation down to step depth
G3 X20.000 Y13.000 Z-11.196 I-8.000 F100.00;
G3 X20.000 Y13.000 Z-12.643 I-8.000 F100.00;
G3 X20.000 Y13.000 Z-12.643 I-8.000 F100.00; Final full pass at depth
; Spiral in to final radius in 2.000mm passes
G3 X6.000 Y13.000 I-7.000 F100.00;
G3 X18.000 Y13.000 I6.000 F100.00;
G3 X6.000 Y13.000 I-6.000 F100.00; Complete circle at final radius
G0 X5.000 Z-12.393; Move cutter away from wall
G0 Z10.000;
G0 X20.000;
;
G0 X20.000 Y13.000 Z-12.643; Move to hole start position
; Helical interpolation down to step depth
G3 X20.000 Y13.000 Z-14.089 I-8.000 F100.00;
G3 X20.000 Y13.000 Z-15.536 I-8.000 F100.00;
G3 X20.000 Y13.000 Z-15.536 I-8.000 F100.00; Final full pass at depth
; Spiral in to final radius in 2.000mm passes
G3 X6.000 Y13.000 I-7.000 F100.00;
G3 X18.000 Y13.000 I6.000 F100.00;
G3 X6.000 Y13.000 I-6.000 F100.00; Complete circle at final radius
G0 X5.000 Z-15.286; Move cutter away from wall
G0 Z10.000;
G0 X20.000;
;
G0 X20.000 Y13.000 Z-15.536; Move to hole start position
; Helical interpolation down to step depth
G3 X20.000 Y13.000 Z-16.982 I-8.000 F100.00;
G3 X20.000 Y13.000 Z-18.429 I-8.000 F100.00;
G3 X20.000 Y13.000 Z-18.429 I-8.000 F100.00; Final full pass at depth
; Spiral in to final radius in 2.000mm passes
G3 X6.000 Y13.000 I-7.000 F100.00;
G3 X18.000 Y13.000 I6.000 F100.00;
G3 X6.000 Y13.000 I-6.000 F100.00; Complete circle at final radius
G0 X5.000 Z-18.179; Move cutter away from wall
G0 Z10.000;
G0 X20.000;
;
G0 X20.000 Y13.000 Z-18.429; Move to hole start position
; Helical interpolation down to step depth
G3 X20.000 Y13.000 Z-19.875 I-8.000 F100.00;
G3 X20.000 Y13.000 Z-21.321 I-8.000 F100.00;
G3 X20.000 Y13.000 Z-21.321 I-8.000 F100.00; Final full pass at depth
; Spiral in to final radius in 2.000mm passes
G3 X6.000 Y13.000 I-7.000 F100.00;
G3 X18.000 Y13.000 I6.000 F100.00;
G3 X6.000 Y13.000 I-6.000 F100.00; Complete circle at final radius
G0 X5.000 Z-21.071; Move cutter away from wall
G0 Z10.000;
G0 X20.000;
;
G0 X20.000 Y13.000 Z-21.321; Move to hole start position
; Helical interpolation down to step depth
G3 X20.000 Y13.000 Z-22.768 I-8.000 F100.00;
G3 X20.000 Y13.000 Z-24.214 I-8.000 F100.00;
G3 X20.000 Y13.000 Z-24.214 I-8.000 F100.00; Final full pass at depth
; Spiral in to final radius in 2.000mm passes
G3 X6.000 Y13.000 I-7.000 F100.00;
G3 X18.000 Y13.000 I6.000 F100.00;
G3 X6.000 Y13.000 I-6.000 F100.00; Complete circle at final radius
G0 X5.000 Z-23.964; Move cutter away from wall
G0 Z10.000;
G0 X20.000;
;
G0 X20.000 Y13.000 Z-24.214; Move to hole start position
; Helical interpolation down to step depth
G3 X20.000 Y13.000 Z-25.661 I-8.000 F100.00;
G3 X20.000 Y13.000 Z-27.107 I-8.000 F100.00;
G3 X20.000 Y13.000 Z-27.107 I-8.000 F100.00; Final full pass at depth
; Spiral in to final radius in 2.000mm passes
G3 X6.000 Y13.000 I-7.000 F100.00;
G3 X18.000 Y13.000 I6.000 F100.00;
G3 X6.000 Y13.000 I-6.000 F100.00; Complete circle at final radius
G0 X5.000 Z-26.857; Move cutter away from wall
G0 Z10.000;
G0 X20.000;
;
G0 X20.000 Y13.000 Z-27.107; Move to hole start position
; Helical interpolation down to step depth
G3 X20.000 Y13.000 Z-28.554 I-8.000 F100.00;
G3 X20.000 Y13.000 Z-30.000 I-8.000 F100.00;
G3 X20.000 Y13.000 Z-30.000 I-8.000 F100.00; Final full pass at depth
; Spiral in to final radius in 2.000mm passes
G3 X6.000 Y13.000 I-7.000 F100.00;
G3 X18.000 Y13.000 I6.000 F100.00;
G3 X6.000 Y13.000 I-6.000 F100.00; Complete circle at final radius
;
G0 X5.000 Z-29.750; Move cutter away from wall
G0 Z10.000; Clear tool
;
M5; Stop spindle
M2; End program