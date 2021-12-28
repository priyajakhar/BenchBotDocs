import argparse, sys, time
sys.path.append("../..")
from MachineMotion import *

parser = argparse.ArgumentParser()
parser.add_argument('-s', type=int)
parser.add_argument('-t', type=int)
args = parser.parse_args()
speed = args.s
acc = speed/2

mm = MachineMotion()
mm.releaseEstop()
mm.resetSystem()

axesToMove = [2,3]
for axis in axesToMove:
    mm.configAxis(axis, MICRO_STEPS.ustep_8, MECH_GAIN.enclosed_timing_belt_mm_turn)

mm.moveContinuous(axesToMove, speed, acc)
time.sleep(args.t)

mm.stopMoveContinuous(axesToMove, 10)
time.sleep(1)