import sys, time
sys.path.append("../..")
from MachineMotion import *

mm = MachineMotion()
mm.releaseEstop()
mm.resetSystem()

mm.configAxis([2,3], MICRO_STEPS.ustep_8, MECH_GAIN.roller_conveyor_mm_turn)

mm.moveContinuous([2,3], 25, 10)
time.sleep(1)

mm.stopMoveContinuous([2,3], 10)
time.sleep(1)