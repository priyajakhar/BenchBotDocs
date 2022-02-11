import sys, numpy as np, tkinter as tk
sys.path.append("..")
from MachineMotion import *
from tkinter import *

mm = MachineMotion(DEFAULT_IP_ADDRESS.usb_windows)
axesToMove = [2,3]
directions = ["positive","negative"]
mechGain = MECH_GAIN.enclosed_timing_belt_mm_turn
for axis in axesToMove:
    mm.configAxis(axis, MICRO_STEPS.ustep_8, mechGain)
mm.emitAcceleration(25)

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        
        def start():
            mm.releaseEstop()
            mm.resetSystem()
        
        def createNewWindow():
            newWindow = tk.Toplevel()
            newWindow.title("Free Control")
            newWindow.geometry("200x200")
            
            def handler1(e):
                x = np.clip((e.x - 100), -50, 50)
                y = np.clip((100 - e.y), -50, 50)
                speed = abs(y)
                mm.emitSpeed(speed)
                if x > 0:
                    pos = [(50-x)/10, (50+x)/10]
                else:
                    pos = [-1*(x-50)/10, (50+x)/10]
                if y<0:
                    positions = [-1*pos[0], -1*pos[1]]
                else:
                    positions = pos
                #print('{}'.format(positions))
                mm.emitCombinedAxisRelativeMove(axesToMove, directions, positions)
            newWindow.bind('<B1-Motion>', handler1)
        
        def check():
            d = dist.get()
            if d == '':
                d = 10
            else:
                d = int(d)
                if d>500:
                    d = 5000
                elif d<1:
                    d = 10
                else:
                    d=d*10
            s = sped.get()
            if s == '':
                s = 10
            else:
                s = int(s)
                s=s*10
            return d, s

        def forward():
            d, s = check()
            positions = [d, d]
            mm.emitSpeed(s)
            mm.emitCombinedAxisRelativeMove(axesToMove, directions, positions)
            mm.waitForMotionCompletion()

        def backward():
            d, s = check()
            pos = -1 * (d)
            positions = [pos, pos]
            mm.emitSpeed(s)
            mm.emitCombinedAxisRelativeMove(axesToMove, directions, positions)
            mm.waitForMotionCompletion()
        
        def stop():
            mm.triggerEstop()

        self.title("Benchbot App")
        self.geometry("540x242")
        self.resizable(False, False)

        btnstart = Button(self, text="START", bg="green", fg="white", command=start).grid(column=0, row=0)
        heading = Label(self, text="Move the bot").grid(column=1, row=1, sticky=W)
        labeldist = Label(self, text="Distance (in cm)").grid(column=2, row=3, sticky=W)

        def validate(P):
            if str.isdigit(P) or P == "":
                return True
            else:
                return False
        vcmd = self.register(validate)
        dist = Entry(self, validate='key', validatecommand=(vcmd, '%P'), width=5, justify='right')
        dist.insert(END, '10')
        dist.grid(column=3, row=3, sticky=E)
        
        labelspd = Label(self, text="Speed (in cm/rev)").grid(column=2, row=4, sticky=W)
        s = StringVar()
        
        sped = Spinbox(self, from_=10, to=100, width=5, justify='right', textvariable=s, validate='key', validatecommand=(vcmd, '%P'))
        sped.grid(column=3, row=4, sticky=E)
        spbar = Scale(self, from_=10, to=100, orient=HORIZONTAL, showvalue=0, sliderlength=10, variable=s).grid(column=5, row=4)

        btnf = Button(self, text=" Forward  ", bg="white", fg="black", command=forward).grid(column=2, row=5, sticky=E)
        btnb = Button(self, text="Backward", bg="white", fg="black", command=backward).grid(column=2, row=7, sticky=E)
        btnjsc = Button(self, text="Free Control", bg="blue", fg="white", command=createNewWindow).grid(column=1, row=10, sticky=E)

        btnstop = Button(self, text="STOP", bg="red", fg="white", command=stop).grid(column=0, row=12, sticky=SW)
        btnquit = Button(self, text="QUIT", command=self.destroy).grid(column=10, row=12, sticky=SE)
  
if __name__ == "__main__":
    root = Window()
    #root.iconphoto(False, tk.PhotoImage(file='bb.png'))
    root.mainloop()