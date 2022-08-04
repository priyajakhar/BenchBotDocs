import sys, time, os, tkinter as tk, threading, pandas as pd
sys.path.append("..")
from MachineMotion import *
from tkinter import *

mm = MachineMotion(DEFAULT_IP_ADDRESS.usb_windows)
camMotor = 1
mm.configAxis(camMotor, MICRO_STEPS.ustep_8, MECH_GAIN.ballscrew_10mm_turn)
mm.configAxisDirection(camMotor, DIRECTION.POSITIVE)

wheelMotors = [2,3]
directions = ["positive","negative"]
for axis in wheelMotors:
    mm.configAxis(axis, MICRO_STEPS.ustep_8, MECH_GAIN.enclosed_timing_belt_mm_turn)
    mm.configAxisDirection(axis, directions[axis-2])
mm.emitAcceleration(50)
mm.emitSpeed(150)
global stop_exec
path = os.getcwd()+'\\out\\build\\x64-Debug\\RemoteCli.exe'

#For reading images to be clicked per row values
df  = pd.read_excel('weeds.xlsx')
colvalues = df[['pics to take']].values
i = 0
pots = [None] * colvalues.size
for num in colvalues:
	pots[i] = num[0]
	i = i+1

sp = os.getcwd()+'\\Images'
if not os.path.exists(sp):
    os.system('mkdir Images')

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
               
        def start():
            mm.releaseEstop()
            mm.resetSystem()
            #For changing location of image storage
            os.chdir(sp)
        
        def startcollec():
            global stop_exec
            stop_exec = False
            dist = int(rdist.get())*10 #distance between rows of pots
            positions = [dist, dist] #position variable
            for j in pots:
                if j==0:
                    mm.moveRelativeCombined(wheelMotors, positions)
                    mm.waitForMotionCompletion()
                    continue
                else:
                    c = int(600/(j-1)) #total distance between home and end sensor
                    for i in range(1,j):
                        if stop_exec:
                            break
                        #Trigger capture of image
                        os.startfile(path)
                        time.sleep(15)
                        #Move camera plate to next point
                        mm.moveRelative(camMotor, c)
                        mm.waitForMotionCompletion()
                    if stop_exec:
                        break
                    #Trigger image capture at last point
                    os.startfile(path)
                    time.sleep(15)    
                    #move camera plate to start location
                    mm.moveToHome(camMotor)
                    mm.waitForMotionCompletion()
                    #move the bot to next set of pots
                    mm.moveRelativeCombined(wheelMotors, positions)
                    mm.waitForMotionCompletion()
                   
        def stop():
            global stop_exec
            stop_exec = True
            mm.moveToHome(camMotor)
            mm.waitForMotionCompletion()
            mm.triggerEstop()

        self.title("Benchbot App")
        self.geometry("350x250")
        self.resizable(False, False)

        def validate(P):
            if str.isdigit(P) or P == "":
                return True
            else:
                return False
        vcmd = self.register(validate)

        Button(self, text='START', bg="green", fg="black", command=start).place(x=10,y=10)
        Label(self, text="Distance between rows (cm)").place(x=30,y=70)
        rdist = Entry(self, validate='key', validatecommand=(vcmd, '%P'), width=5, justify='right')
        rdist.insert(END, '30')
        rdist.place(x=270,y=70)
        Button(self, text="Begin Data Collection", bg="white", fg="black", command=lambda:threading.Thread(target=startcollec).start()).place(x=50,y=120)
        Button(self, text='STOP', bg="red", fg="black", command=lambda:threading.Thread(target=stop).start()).place(x=10,y=190)
       
if __name__ == "__main__":
    root = Window()
    root.mainloop()