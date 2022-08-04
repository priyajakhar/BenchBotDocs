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
mm.emitSpeed(40)
path = os.getcwd()+'\\out\\build\\x64-Debug\\RemoteCli.exe'

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.backGroundImage=PhotoImage(file="bg.png")
        self.backGroundImageLabel=Label(self,image=self.backGroundImage)
        self.backGroundImageLabel.place(x=0,y=0)
        self.canvas = Canvas(self, width=350, height=300, bg='#57C5BD').place(x=355,y=30)
        
        def start():
            mm.releaseEstop()
            mm.resetSystem()
            os.chdir(os.getcwd()+'\\Images')
        
        def startcollec():
            global stop_exec
            stop_exec = False
            c = cdist.get()
            ct = ctotal.get()
            r = rdist.get()
            rt = rtotal.get()

            if (r=='' or c=='' or rt=='' or ct==''):
                print('Please enter all values')

            else:
                r = int(r)*10
                positions = [r, r]
                c = int(c)*10
                rt = int(rt)
                ct = int(ct)
                for i in range(0,rt):
                    #move the camera over the pots
                    if stop_exec:
                        break
                    os.startfile(path)
                    time.sleep(15)
                    for j in range(1,ct):
                        if stop_exec:
                            break
                        #Trigger capture of image
                        mm.moveRelative(camMotor, c)
                        mm.waitForMotionCompletion()
                        os.startfile(path)
                        time.sleep(15)
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

        self.title("Benchbot")
        self.geometry("800x420")
        self.resizable(False, False)

        self.start_btn = PhotoImage(file="start.png")
        Button(self, image=self.start_btn, borderwidth=0, command=start).place(x=360,y=280)
        Label(self, text="Data Acquisition", font="Playfair 20 bold", bg='#57C5BD').place(x=360,y=35)
        
        def validate(P):
            if str.isdigit(P) or P == "":
                return True
            else:
                return False
        vcmd = self.register(validate)

        Label(self, text="Distance between rows (cm)", bg='#57C5BD').place(x=380,y=90)
        rdist = Entry(self, borderwidth=0, validate='key', validatecommand=(vcmd, '%P'), width=5, justify='right')
        rdist.insert(END, '10')
        rdist.place(x=620,y=90)
        
        Label(self, text="Distance between columns (cm)", bg='#57C5BD').place(x=380,y=120)
        cdist = Entry(self, borderwidth=0, validate='key', validatecommand=(vcmd, '%P'), width=5, justify='right')
        cdist.insert(END, '10')
        cdist.place(x=620,y=120)

        Label(self, text="Row count", bg='#57C5BD').place(x=380,y=150)
        rtotal = Entry(self, borderwidth=0, validate='key', validatecommand=(vcmd, '%P'), width=5, justify='right')
        rtotal.insert(END, '1')
        rtotal.place(x=620,y=150)

        Label(self, text="Column count", bg='#57C5BD').place(x=380,y=180)
        ctotal = Entry(self, borderwidth=0, validate='key', validatecommand=(vcmd, '%P'), width=5, justify='right')
        ctotal.insert(END, '1')
        ctotal.place(x=620,y=180)

        Button(self, text=" Begin Data Collection  ", bg="white", fg="black", command=lambda:threading.Thread(target=startcollec).start()).place(x=450,y=220)
        
        self.stop_btn = PhotoImage(file="stop.png")
        Button(self, image=self.stop_btn, borderwidth=0, command=lambda:threading.Thread(target=stop).start()).place(x=500,y=280)
        self.quit_btn = PhotoImage(file="quit.png")
        Button(self, image=self.quit_btn, borderwidth=0, command=self.destroy).place(x=625,y=280)
        
if __name__ == "__main__":
    root = Window()
    root.iconphoto(False, tk.PhotoImage(file='icon.png'))
    root.mainloop()