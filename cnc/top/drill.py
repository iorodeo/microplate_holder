from __future__ import print_function
import os 
import sys
from py2gcode import gcode_cmd
from py2gcode import cnc_dxf

feedrate = 50.0
fileName = 'top_in.dxf'
stockThickness = 0.51
drillMargin =0.5*0.125

startZ = 0.0
stopZ = -(stockThickness + drillMargin)
safeZ = 0.3
stepZ = 0.05
startDwell = 0.5

prog = gcode_cmd.GCodeProg()
prog.add(gcode_cmd.GenericStart())
prog.add(gcode_cmd.Space())
prog.add(gcode_cmd.FeedRate(feedrate))

param = { 
        'fileName'    : fileName,
        #'layers'      : ['mount_holes', 'fixturing_holes'],
        'layers'      : ['mount_holes'],
        'dxfTypes'    : ['CIRCLE'],
        'startZ'      : startZ,
        'stopZ'       : stopZ,
        'safeZ'       : safeZ,
        'stepZ'       : stepZ,
        'startDwell'  : startDwell,
        }
drill = cnc_dxf.DxfDrill(param)
prog.add(drill)

prog.add(gcode_cmd.Space())
prog.add(gcode_cmd.End(),comment=True)
baseName, dummy = os.path.splitext(__file__)
fileName = '{0}.ngc'.format(baseName)
print('generating: {0}'.format(fileName))
prog.write(fileName)
