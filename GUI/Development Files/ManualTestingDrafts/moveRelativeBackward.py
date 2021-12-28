import argparse, sys
sys.path.append("../..")
from MachineMotion import *

parser = argparse.ArgumentParser()
parser.add_argument('-d', type=int)
args = parser.parse_args()

mm = MachineMotion()
mm.releaseEstop()
mm.resetSystem()

axesToMove = [2,3]
for axis in axesToMove:
    mm.configAxis(axis, MICRO_STEPS.ustep_8, MECH_GAIN.enclosed_timing_belt_mm_turn)

distances = [args.d, args.d]*(-1)
mm.moveRelativeCombined(axesToMove, distances)
mm.waitForMotionCompletion()