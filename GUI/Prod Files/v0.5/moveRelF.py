#Move Relative Combined

import sys
sys.path.append("..")
from MachineMotion import *

mm = MachineMotion(DEFAULT_IP_ADDRESS.usb_windows)
#mm.releaseEstop()
#mm.resetSystem()

axesToMove = [2,3]
directions = ["positive","negative"]
positions = [50, 50]
mechGain = MECH_GAIN.enclosed_timing_belt_mm_turn

for axis in axesToMove:
    mm.configAxis(axis, MICRO_STEPS.ustep_8, mechGain)
    
mm.emitSpeed(50)
mm.emitAcceleration(25)

mm.emitCombinedAxisRelativeMove(axesToMove, directions, positions)
mm.waitForMotionCompletion()