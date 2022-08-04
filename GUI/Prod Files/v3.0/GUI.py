import sys, time, os, tkinter as tk, threading
sys.path.append("..")
from MachineMotion import *
from tkinter import *

global stop_exec
mm = MachineMotion(DEFAULT_IP_ADDRESS.usb_windows)
wheelMotors = [2,3]
directions = ["positive","negative"]
for axis in wheelMotors:
    mm.configAxis(axis, MICRO_STEPS.ustep_8, MECH_GAIN.enclosed_timing_belt_mm_turn)
    mm.configAxisDirection(axis, directions[axis-2])
camMotor = 1
mm.configAxis(camMotor, MICRO_STEPS.ustep_8, MECH_GAIN.ballscrew_10mm_turn)
mm.configAxisDirection(camMotor, DIRECTION.POSITIVE)
mm.emitAcceleration(25)
mm.emitSpeed(50)

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        
        def start():
            mm.releaseEstop()
            mm.resetSystem()
        
        def startcollec():
            global stop_exec
            stop_exec = False
            r = rdist.get()
            c = cdist.get()
            rt = rtotal.get()
            ct = ctotal.get()

            if (r=='' or c=='' or rt=='' or ct==''):
                print('Please enter all values')

            else:
                r = int(r)*10
                positions = [r, r]
                c = int(c)*10
                rt = int(rt)
                ct = int(ct)
                #for each row on the table
                for i in range(0,rt):
                    #move the camera over the pots
                    if stop_exec:
                        break
                    for j in range(0,ct):
                        if stop_exec:
                            break
                        #Trigger capture of image
                        os.startfile(r"C:\Users\Priya\Documents\SDK\out\build\x64-Debug\RemoteCli.exe")
                        mm.moveRelative(camMotor, c)
                        mm.waitForMotionCompletion()
                        time.sleep(10)
                    #move camera plate to start location
                    mm.moveToHome(camMotor)
                    mm.waitForMotionCompletion()
                    #move the bot to next row
                    mm.moveRelativeCombined(wheelMotors, positions)
                    mm.waitForMotionCompletion()
    
        def stop():
            global stop_exec
            stop_exec = True
            mm.moveToHome(camMotor)
            mm.waitForMotionCompletion()
            mm.triggerEstop()

        self.title("Benchbot App")
        self.geometry("540x242")
        self.resizable(False, False)

        Button(self, text="START", bg="green", fg="white", command=start).grid(column=0, row=0)
        Label(self, text="Move the bot").grid(column=1, row=1, sticky=W)

        def validate(P):
            if str.isdigit(P) or P == "":
                return True
            else:
                return False
        vcmd = self.register(validate)

        Label(self, text="Distance between rows (cm)").grid(column=2, row=3, sticky=W)
        rdist = Entry(self, validate='key', validatecommand=(vcmd, '%P'), width=5, justify='right')
        rdist.insert(END, '10')
        rdist.grid(column=3, row=3, sticky=E)
        
        Label(self, text="Distance between columns (cm)").grid(column=2, row=4, sticky=W)
        cdist = Entry(self, validate='key', validatecommand=(vcmd, '%P'), width=5, justify='right')
        cdist.insert(END, '10')
        cdist.grid(column=3, row=4, sticky=E)

        Label(self, text="Total row count").grid(column=2, row=5, sticky=W)
        rtotal = Entry(self, validate='key', validatecommand=(vcmd, '%P'), width=5, justify='right')
        rtotal.insert(END, '10')
        rtotal.grid(column=3, row=5, sticky=E)

        Label(self, text="Total column count").grid(column=2, row=6, sticky=W)
        ctotal = Entry(self, validate='key', validatecommand=(vcmd, '%P'), width=5, justify='right')
        ctotal.insert(END, '10')
        ctotal.grid(column=3, row=6, sticky=E)

        Button(self, text=" Start Data Collection  ", bg="white", fg="black", command=lambda:threading.Thread(target=startcollec).start()).grid(column=2, row=8, sticky=E)
        Button(self, text="STOP", bg="red", fg="white", command=lambda:threading.Thread(target=stop).start()).grid(column=0, row=12, sticky=SW)
        Button(self, text="QUIT", command=self.destroy).grid(column=10, row=12, sticky=SE)
  
if __name__ == "__main__":
    root = Window()
    root.mainloop()
