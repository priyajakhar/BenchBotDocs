#Move Relative Combined

import sys, argparse
sys.path.append("..")
from MachineMotion import *

parser = argparse.ArgumentParser()
parser.add_argument('-d', type=int)
parser.add_argument('-s', type=int)
args = parser.parse_args()

mm = MachineMotion(DEFAULT_IP_ADDRESS.usb_windows)
#mm.releaseEstop()
#mm.resetSystem()

axesToMove = [2,3]
directions = ["positive","negative"]
positions = [args.d, args.d]
mechGain = MECH_GAIN.enclosed_timing_belt_mm_turn

for axis in axesToMove:
    mm.configAxis(axis, MICRO_STEPS.ustep_8, mechGain)
    
mm.emitSpeed(args.s)
mm.emitAcceleration(25)

mm.emitCombinedAxisRelativeMove(axesToMove, directions, positions)
mm.waitForMotionCompletion()