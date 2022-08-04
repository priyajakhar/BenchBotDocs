import sys, time, os, tkinter as tk, threading
sys.path.append("..")
from MachineMotion import *
from tkinter import *

mm = MachineMotion(DEFAULT_IP_ADDRESS.usb_windows)
camMotor = 1
mm.configAxis(camMotor, MICRO_STEPS.ustep_8, MECH_GAIN.ballscrew_10mm_turn)
mm.configAxisDirection(camMotor, DIRECTION.POSITIVE)
mm.emitAcceleration(50)
mm.emitSpeed(50)
path = os.getcwd()+'\\out\\build\\x64-Debug\\RemoteCli.exe'

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        
        coutl = StringVar()
        coutl.set('Welcome')
        def poweron():
            mm.releaseEstop()
            mm.resetSystem()
            coutl.set('Powered On')

        def updatespeed():
            s = sbox.get()
            speed = int(s)
            mm.emitSpeed(speed)
            coutl.set('Speed set to '+s)

        def updateacc():
            a = abox.get()
            acceleration = int(a)
            mm.emitAcceleration(acceleration)
            coutl.set('Acceleration set to '+a)

        def moveforward():
            distance = dist.get()
            distance = int(distance)*10
            mm.moveRelative(camMotor, distance)
            mm.waitForMotionCompletion()
            coutl.set('Moved by '+str(distance)+' mm')

        def movebackward():
            distance = dist.get()
            distance = int(distance)*(-10)
            mm.moveRelative(camMotor, distance)
            mm.waitForMotionCompletion()
            coutl.set('Moved by '+str(distance)+' mm')

        def getdistances():
            current_position = mm.getCurrentPositions()[1]
            coutl.set('Current position is '+str(current_position)+' mm')

        def gohome():
            mm.moveToHome(camMotor)
            mm.waitForMotionCompletion()
            coutl.set('Homed')
        
        def captureimage():
            os.startfile(path)
            time.sleep(14)
            coutl.set('Image Captured')

        def poweroff():
            mm.waitForMotionCompletion()
            mm.triggerEstop()
            coutl.set('Powered Off')

        self.title("Testing App")
        self.geometry("650x250")
        self.resizable(False, False)

        Button(self, text="Power On", bg="green", fg="white", command=poweron).grid(column=0, row=0)
        
        def validate(P):
            if str.isdigit(P) or P == "":
                return True
            else:
                return False
        vcmd = self.register(validate)
        
        Label(self, text="Speed").grid(column=1, row=3, sticky=W)
        sbox = Entry(self, validate='key', validatecommand=(vcmd, '%P'), width=5, justify='right')
        sbox.insert(END, '10')
        sbox.grid(column=3, row=3, sticky=E)
        Button(self, text="Set Speed", command=updatespeed).grid(column=5, row=3, sticky=W)

        Label(self, text="Acceleration").grid(column=1, row=4, sticky=W)
        abox = Entry(self, validate='key', validatecommand=(vcmd, '%P'), width=5, justify='right')
        abox.insert(END, '5')
        abox.grid(column=3, row=4, sticky=E)
        Button(self, text="Set Acceleration", command=updateacc).grid(column=5, row=4, sticky=W)
        
        Label(self, text="Distance (cm)").grid(column=1, row=5, sticky=W)
        dist = Entry(self, validate='key', validatecommand=(vcmd, '%P'), width=5, justify='right')
        dist.insert(END, '10')
        dist.grid(column=3, row=5, sticky=E)
        Button(self, text="Move Forward", command=moveforward).grid(column=5, row=5, sticky=W)
        Button(self, text="Move Backward", command=movebackward).grid(column=7, row=5, sticky=W)

        Button(self, text="Get Home Distance", command=getdistances).grid(column=1, row=6, sticky=W)
        Button(self, text="Go Home", command=gohome).grid(column=5, row=6, sticky=W)

        Button(self, text="Capture Image", command=captureimage).grid(column=1, row=7, sticky=W)
         
        # output label
        Label(self, textvariable=coutl, bg="white", width=30).place(x=200,y=210)
        
        Button(self, text="Power Off", bg="red", fg="white", command=poweroff).grid(column=0, row=12, sticky=SW)
        Button(self, text="QUIT", command=self.destroy).grid(column=10, row=12, sticky=SE)
  
if __name__ == "__main__":
    root = Window()
    root.mainloop()