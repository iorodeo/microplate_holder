from __future__ import print_function
import os 
import sys
from py2gcode import gcode_cmd
from py2gcode import cnc_dxf

feedrate = 150.0
fileName = 'bottom_in.dxf'
finishDepth = 0.56
roughDepth = 0.5
startZ = 0.0
safeZ = 0.5
maxCutDepth = 0.05
toolDiam = 0.375 
direction = 'ccw'
cutterComp = 'outside'
startDwell = 1.0
startCond = 'minX'

prog = gcode_cmd.GCodeProg()
prog.add(gcode_cmd.GenericStart())
prog.add(gcode_cmd.Space())
prog.add(gcode_cmd.FeedRate(feedrate))

prog.add(gcode_cmd.PathBlendMode(P=0.01))

roughParam = {
        'fileName'    : fileName,
        'layers'      : ['rough_boundary'],
        'depth'       : roughDepth,
        'startZ'      : startZ,
        'safeZ'       : safeZ,
        'toolDiam'    : toolDiam,
        'direction'   : direction,
        'cutterComp'  : cutterComp,
        'maxCutDepth' : maxCutDepth,
        'startDwell'  : startDwell, 
        'startCond'   : startCond,
        }
roughBoundary = cnc_dxf.DxfBoundary(roughParam)
prog.add(roughBoundary)

finishParam = {
        'fileName'    : fileName,
        'layers'      : ['boundary'],
        'depth'       : finishDepth,
        'startZ'      : startZ,
        'safeZ'       : safeZ,
        'toolDiam'    : toolDiam,
        'direction'   : direction,
        'cutterComp'  : cutterComp,
        'maxCutDepth' : maxCutDepth,
        'startDwell'  : startDwell, 
        'startCond'   : startCond,
        }
finishBoundary = cnc_dxf.DxfBoundary(finishParam)
prog.add(finishBoundary)

prog.add(gcode_cmd.ExactPathMode())

prog.add(gcode_cmd.Space())
prog.add(gcode_cmd.End(),comment=True)
baseName, dummy = os.path.splitext(__file__)
fileName = '{0}.ngc'.format(baseName)
print('generating: {0}'.format(fileName))
prog.write(fileName)
