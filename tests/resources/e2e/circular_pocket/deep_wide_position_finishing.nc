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
;     "finishing_pass": 0.5,
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
G2 X14.000 Y13.000 Z-10.329 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-10.907 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-11.486 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-12.064 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-12.643 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-12.643 I-2.000 F100.00; Final full pass at depth
; Spiral out to final radius in 1.875mm passes
G2 X8.125 Y13.000 I-2.938 F100.00;
G2 X15.875 Y13.000 I3.875 F100.00;
G2 X6.250 Y13.000 I-4.812 F100.00;
G2 X17.750 Y13.000 I5.750 F100.00;
G2 X4.375 Y13.000 I-6.688 F100.00;
G2 X19.625 Y13.000 I7.625 F100.00;
G2 X2.500 Y13.000 I-8.562 F100.00;
G2 X21.500 Y13.000 I9.500 F100.00;
G2 X2.500 Y13.000 I-9.500 F100.00; Complete circle at final radius
G0 X3.500 Z-12.393; Move cutter away from wall
;
G0 X14.000 Y13.000 Z-12.643; Move to hole start position
; Helical interpolation down to step depth
G2 X14.000 Y13.000 Z-13.221 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-13.800 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-14.379 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-14.957 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-15.536 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-15.536 I-2.000 F100.00; Final full pass at depth
; Spiral out to final radius in 1.875mm passes
G2 X8.125 Y13.000 I-2.938 F100.00;
G2 X15.875 Y13.000 I3.875 F100.00;
G2 X6.250 Y13.000 I-4.812 F100.00;
G2 X17.750 Y13.000 I5.750 F100.00;
G2 X4.375 Y13.000 I-6.688 F100.00;
G2 X19.625 Y13.000 I7.625 F100.00;
G2 X2.500 Y13.000 I-8.562 F100.00;
G2 X21.500 Y13.000 I9.500 F100.00;
G2 X2.500 Y13.000 I-9.500 F100.00; Complete circle at final radius
G0 X3.500 Z-15.286; Move cutter away from wall
;
G0 X14.000 Y13.000 Z-15.536; Move to hole start position
; Helical interpolation down to step depth
G2 X14.000 Y13.000 Z-16.114 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-16.693 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-17.271 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-17.850 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-18.429 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-18.429 I-2.000 F100.00; Final full pass at depth
; Spiral out to final radius in 1.875mm passes
G2 X8.125 Y13.000 I-2.938 F100.00;
G2 X15.875 Y13.000 I3.875 F100.00;
G2 X6.250 Y13.000 I-4.812 F100.00;
G2 X17.750 Y13.000 I5.750 F100.00;
G2 X4.375 Y13.000 I-6.688 F100.00;
G2 X19.625 Y13.000 I7.625 F100.00;
G2 X2.500 Y13.000 I-8.562 F100.00;
G2 X21.500 Y13.000 I9.500 F100.00;
G2 X2.500 Y13.000 I-9.500 F100.00; Complete circle at final radius
G0 X3.500 Z-18.179; Move cutter away from wall
;
G0 X14.000 Y13.000 Z-18.429; Move to hole start position
; Helical interpolation down to step depth
G2 X14.000 Y13.000 Z-19.007 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-19.586 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-20.164 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-20.743 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-21.321 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-21.321 I-2.000 F100.00; Final full pass at depth
; Spiral out to final radius in 1.875mm passes
G2 X8.125 Y13.000 I-2.938 F100.00;
G2 X15.875 Y13.000 I3.875 F100.00;
G2 X6.250 Y13.000 I-4.812 F100.00;
G2 X17.750 Y13.000 I5.750 F100.00;
G2 X4.375 Y13.000 I-6.688 F100.00;
G2 X19.625 Y13.000 I7.625 F100.00;
G2 X2.500 Y13.000 I-8.562 F100.00;
G2 X21.500 Y13.000 I9.500 F100.00;
G2 X2.500 Y13.000 I-9.500 F100.00; Complete circle at final radius
G0 X3.500 Z-21.071; Move cutter away from wall
;
G0 X14.000 Y13.000 Z-21.321; Move to hole start position
; Helical interpolation down to step depth
G2 X14.000 Y13.000 Z-21.900 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-22.479 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-23.057 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-23.636 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-24.214 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-24.214 I-2.000 F100.00; Final full pass at depth
; Spiral out to final radius in 1.875mm passes
G2 X8.125 Y13.000 I-2.938 F100.00;
G2 X15.875 Y13.000 I3.875 F100.00;
G2 X6.250 Y13.000 I-4.812 F100.00;
G2 X17.750 Y13.000 I5.750 F100.00;
G2 X4.375 Y13.000 I-6.688 F100.00;
G2 X19.625 Y13.000 I7.625 F100.00;
G2 X2.500 Y13.000 I-8.562 F100.00;
G2 X21.500 Y13.000 I9.500 F100.00;
G2 X2.500 Y13.000 I-9.500 F100.00; Complete circle at final radius
G0 X3.500 Z-23.964; Move cutter away from wall
;
G0 X14.000 Y13.000 Z-24.214; Move to hole start position
; Helical interpolation down to step depth
G2 X14.000 Y13.000 Z-24.793 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-25.371 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-25.950 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-26.529 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-27.107 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-27.107 I-2.000 F100.00; Final full pass at depth
; Spiral out to final radius in 1.875mm passes
G2 X8.125 Y13.000 I-2.938 F100.00;
G2 X15.875 Y13.000 I3.875 F100.00;
G2 X6.250 Y13.000 I-4.812 F100.00;
G2 X17.750 Y13.000 I5.750 F100.00;
G2 X4.375 Y13.000 I-6.688 F100.00;
G2 X19.625 Y13.000 I7.625 F100.00;
G2 X2.500 Y13.000 I-8.562 F100.00;
G2 X21.500 Y13.000 I9.500 F100.00;
G2 X2.500 Y13.000 I-9.500 F100.00; Complete circle at final radius
G0 X3.500 Z-26.857; Move cutter away from wall
;
G0 X14.000 Y13.000 Z-27.107; Move to hole start position
; Helical interpolation down to step depth
G2 X14.000 Y13.000 Z-27.686 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-28.264 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-28.843 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-29.421 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-30.000 I-2.000 F100.00;
G2 X14.000 Y13.000 Z-30.000 I-2.000 F100.00; Final full pass at depth
; Spiral out to final radius in 1.875mm passes
G2 X8.125 Y13.000 I-2.938 F100.00;
G2 X15.875 Y13.000 I3.875 F100.00;
G2 X6.250 Y13.000 I-4.812 F100.00;
G2 X17.750 Y13.000 I5.750 F100.00;
G2 X4.375 Y13.000 I-6.688 F100.00;
G2 X19.625 Y13.000 I7.625 F100.00;
G2 X2.500 Y13.000 I-8.562 F100.00;
G2 X21.500 Y13.000 I9.500 F100.00;
G2 X2.500 Y13.000 I-9.500 F100.00; Complete circle at final radius
;
; Finishing pass of 0.500mm
G2 X22.000 Y13.000 I9.750 F100.00; Spiral out to finishing pass
G2 X22.000 Y13.000 I-10.000 F100.00; Complete circle at final radius
G0 X21.000 Z-29.750; Move cutter away from wall
G0 Z10.000; Clear tool
;
M5; Stop spindle
M2; End program