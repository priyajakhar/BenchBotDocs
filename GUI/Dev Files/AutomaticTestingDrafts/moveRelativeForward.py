import sys
sys.path.append("../..")
from MachineMotion import *

mm = MachineMotion()
mm.releaseEstop()
mm.resetSystem()

axesToMove = [2,3]
for axis in axesToMove:
    mm.configAxis(axis, MICRO_STEPS.ustep_8, MECH_GAIN.roller_conveyor_mm_turn)

distances = [50, 50]
mm.moveRelativeCombined(axesToMove, distances)
mm.waitForMotionCompletion()