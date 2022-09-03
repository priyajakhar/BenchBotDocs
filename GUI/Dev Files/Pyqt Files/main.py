import sys, os
sys.path.append("..")
from MachineMotion import *
mm = MachineMotion(DEFAULT_IP_ADDRESS.usb_windows)
from Tkinter import * 

mm.releaseEstop()
mm.resetSystem()
axesToMove = [2,3]
directions = ["positive","negative"]
mechGain = MECH_GAIN.enclosed_timing_belt_mm_turn
for axis in axesToMove:
    mm.configAxis(axis, MICRO_STEPS.ustep_8, mechGain)
mm.emitSpeed(25)
mm.emitAcceleration(15)
    

running = False
root = Tk()
jobid = None

def start_motor(direction):
    print("starting motor")
    move(direction)

def stop_motor():
    global jobid
    root.after_cancel(jobid)
    print("stopping motor...")
    mm.stopAllMotion()

def move(direction):
    global jobid
    print("Moving %s" % direction)
    if direction == 'forward':
        positions = [10, 10]
        mm.emitCombinedAxisRelativeMove(axesToMove, directions, positions)
    else:
        positions = [-10, -10]
        mm.emitCombinedAxisRelativeMove(axesToMove, directions, positions)
    jobid = root.after(1000, move, direction)

for direction in ("forward", "backward"):
    button = Button(root, text=direction)
    button.pack(side=LEFT)
    button.bind('<ButtonPress-1>', lambda event, direction=direction: start_motor(direction))
    button.bind('<ButtonRelease-1>', lambda event: stop_motor())

root.mainloop()