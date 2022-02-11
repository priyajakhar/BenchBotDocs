import sys, os
sys.path.append("..")
from MachineMotion import *
mm = MachineMotion(DEFAULT_IP_ADDRESS.usb_windows)
from tkinter import *

def start():
    mm.releaseEstop()
    mm.resetSystem()

def forward():
    axesToMove = [2,3]
    directions = ["positive","negative"]
    positions = [dist.get(), dist.get()]
    mechGain = MECH_GAIN.enclosed_timing_belt_mm_turn
    for axis in axesToMove:
        mm.configAxis(axis, MICRO_STEPS.ustep_8, mechGain)
    mm.emitSpeed(sped.get())
    mm.emitAcceleration(25)
    mm.emitCombinedAxisRelativeMove(axesToMove, directions, positions)
    mm.waitForMotionCompletion()

def backward():
    axesToMove = [2,3]
    directions = ["positive","negative"]
    pos = -1 * (dist.get())
    positions = [pos, pos]
    mechGain = MECH_GAIN.enclosed_timing_belt_mm_turn
    for axis in axesToMove:
        mm.configAxis(axis, MICRO_STEPS.ustep_8, mechGain)
    mm.emitSpeed(sped.get())
    mm.emitAcceleration(25)
    mm.emitCombinedAxisRelativeMove(axesToMove, directions, positions)
    mm.waitForMotionCompletion()

def stop():
    mm.triggerEstop()
    
window = Tk()
window.title("Benchbot App")
window.geometry("340x242")
window.resizable(False, False)
window.iconbitmap('./bb.ico')

btnstart = Button(window, text="START", bg="green", fg="white", command=start)
btnstart.grid(column=0, row=0)

lbl1 = Label(window, text="Move the bot")
lbl1.grid(column=1, row=1)

lbl1d = Label(window, text="Distance")
lbl1d.grid(column=1, row=2)

dist = Entry(window, width=3)
dist.grid(column=2, row=2)

lbl1s = Label(window, text="Speed")
lbl1s.grid(column=1, row=3)

sped = Entry(window, width=3)
sped.grid(column=2, row=3)

btn1 = Button(window, text="  Forward  ", bg="white", fg="black", command=forward)
btn1.grid(column=2, row=4)

btn2 = Button(window, text="Backward", bg="white", fg="black", command=backward)
btn2.grid(column=2, row=6)

btnstop = Button(window, text="STOP", bg="red", fg="white", command=stop)
btnstop.grid(column=0, row=8)

btnquit = Button(window, text="Quit", command=window.destroy)
btnquit.grid(column=3, row=9)

window.mainloop()