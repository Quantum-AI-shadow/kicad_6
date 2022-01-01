# kicad_6

## dxf_import

This is a plugin to import dxf file to copper layer as copper zones. Also it will add circle as via in board.

## codes: This folder contains functions for KiCAD 6

fun.py - This has few functions to help scripting.

1. **addZone** -> This function is to create copper zone.

points: This variable is list of list with position arguement, Ex: [[100, 50], [100, 60], [150, 60]]

layerName: This variable is to select the layer in which the copper polygon to be placed, Ex: 'B.Cu'

netName: This variable is to tell the net name of the copper zone, Ex: 'GND'

Ex: ``` addZone([[100, 50], [100, 60], [150, 60]], 'B.Cu', 'GND') ```


2. **addVia** -> This is to create via

pos: This variable is to tell about the position, Ex: [100, 50]

width: This variable is width of the via, Ex: 0.6

drill: Drill of via (drill < width, drill is smaller than width), Ex: 0.4

netName: Net Name, Ex: 'GND'

Ex: ``` addVia([100, 50], 0.6, 0.4, 'GND') ```

3. **addTrack** -> This is to add copper trace in board

start: Start point of the trace, Ex: [100, 50]

end: End point of the trace, Ex: [150, 50]

layerName: Layer name, Ex: 'B.Cu'

netName: Net name, Ex: 'GND'

width: Width of the trace, Ex: 0.5

Ex: ``` addTrack([100, 50], [150, 50], 'B.Cu', 'GND', 0.5) ```
