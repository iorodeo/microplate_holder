from __future__ import print_function
import os 
import sys
from py2gcode import gcode_cmd
from py2gcode import cnc_dxf

# Assumes stock depth is 0.51"

feedrate = 150.0
fileName = 'bottom_in.dxf'

depth = 0.25
roughMargin = 0.01
roughDepth = depth - roughMargin 
startZ = 0.0
safeZ = 0.5
overlap = 0.5
overlapFinish = 0.7
maxCutDepth = 0.05
toolDiam =  0.375 
cornerCut = True 
direction = 'ccw'
startDwell = 1.0

prog = gcode_cmd.GCodeProg()
prog.add(gcode_cmd.GenericStart())
prog.add(gcode_cmd.Space())
prog.add(gcode_cmd.FeedRate(feedrate))

roughParam = {
        'fileName'       : fileName,
        'layers'         : ['rough_pcb_pocket'],
        'components'     : True,
        'depth'          : roughDepth,
        'startZ'         : startZ,
        'safeZ'          : safeZ,
        'overlap'        : overlap,
        'overlapFinish'  : overlap,
        'maxCutDepth'    : maxCutDepth,
        'toolDiam'       : toolDiam,
        'cornerCut'      : cornerCut,
        'direction'      : direction,
        'startDwell'     : startDwell,
        }
roughPocket = cnc_dxf.DxfRectPocketFromExtent(roughParam)
prog.add(roughPocket)

wallFinishParam = {
        'fileName'       : fileName,
        'layers'         : ['pcb_pocket'],
        'components'     : True,
        'depth'          : depth,
        'thickness'      : toolDiam,
        'startZ'         : startZ,
        'safeZ'          : safeZ,
        'overlap'        : overlap,
        'overlapFinish'  : overlap,
        'maxCutDepth'    : maxCutDepth,
        'toolDiam'       : toolDiam,
        'cornerCut'      : cornerCut,
        'direction'      : direction,
        'startDwell'     : startDwell,
        }
wallFinishPocket = cnc_dxf.DxfRectPocketFromExtent(wallFinishParam)
prog.add(wallFinishPocket)

floorFinishParam = {
        'fileName'       : fileName,
        'layers'         : ['pcb_pocket'],
        'components'     : True,
        'depth'          : roughMargin,
        'startZ'         : startZ-roughDepth,
        'safeZ'          : safeZ,
        'overlap'        : overlap,
        'overlapFinish'  : overlapFinish,
        'maxCutDepth'    : maxCutDepth,
        'toolDiam'       : toolDiam,
        'cornerCut'      : cornerCut,
        'direction'      : direction,
        'startDwell'     : startDwell,
        }
floorFinishPocket = cnc_dxf.DxfRectPocketFromExtent(floorFinishParam)
prog.add(floorFinishPocket)

prog.add(gcode_cmd.Space())
prog.add(gcode_cmd.End(),comment=True)
baseName, dummy = os.path.splitext(__file__)
fileName = '{0}.ngc'.format(baseName)
print('generating: {0}'.format(fileName))
prog.write(fileName)
