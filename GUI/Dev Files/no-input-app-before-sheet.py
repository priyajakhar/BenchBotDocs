import sys, time, os, tkinter as tk, threading
sys.path.append("..")
from MachineMotion import *
from tkinter import *

global stop_exec
mm = MachineMotion(DEFAULT_IP_ADDRESS.usb_windows)
camMotor = 1
mm.configAxis(camMotor, MICRO_STEPS.ustep_8, MECH_GAIN.ballscrew_10mm_turn)
mm.configAxisDirection(camMotor, DIRECTION.POSITIVE)
mm.emitAcceleration(25)
mm.emitSpeed(40)
path = os.getcwd()+'\\out\\build\\x64-Debug\\RemoteCli.exe'

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        
        def start():
            mm.releaseEstop()
            mm.resetSystem()
            os.chdir(os.getcwd()+'\\Images')
        
        def startcollec():
            global stop_exec
            stop_exec = False
            totalpots = 6
            c = 690/totalpots
            
            os.startfile(path)
            time.sleep(15)
            for j in range(1,totalpots):
                if stop_exec:
                    break
                mm.moveRelative(camMotor, c)
                mm.waitForMotionCompletion()
                os.startfile(path)
                time.sleep(15)
            mm.moveToHome(camMotor)
            mm.waitForMotionCompletion()
                
        def stop():
            global stop_exec
            stop_exec = True
            mm.moveToHome(camMotor)
            mm.waitForMotionCompletion()
            mm.triggerEstop()

        self.title("Benchbot App")
        self.geometry("150x150")
        self.resizable(False, False)

        Button(self, text='START', bg="green", fg="black", command=start).place(x=10,y=10)
        Button(self, text="Begin Data Collection", bg="white", fg="black", command=lambda:threading.Thread(target=startcollec).start()).place(x=10,y=50)
        Button(self, text='STOP', bg="red", fg="black", command=lambda:threading.Thread(target=stop).start()).place(x=10,y=90)
        
if __name__ == "__main__":
    root = Window()
    root.mainloop()