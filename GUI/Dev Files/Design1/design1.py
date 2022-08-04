import time, tkinter as tk, threading
from tkinter import *

global stop_exec

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.backGroundImage=PhotoImage(file="background.png")
        self.backGroundImageLabel=Label(self,image=self.backGroundImage)
        self.backGroundImageLabel.place(x=0,y=0)
        self.canvas = Canvas(self, width=350, height=300, bg='#57C5BD').place(x=355,y=30)
        #58BA91, DAF7A6
        
        def start():
            print('Start it boy!!')
        
        def startcollec():
            global stop_exec
            stop_exec = False
            
            if False:
                print('Please enter all values')

            else:
                for i in range(0,3):
                    if stop_exec:
                        break
                    for j in range(0,3):
                        if stop_exec:
                            break
                        time.sleep(2)
                        print('Picture clicked')
                        time.sleep(2)
                        print('Moving over')
                    print('Going home')
                 
        def stop():
            global stop_exec
            stop_exec = True
            print('Stooooooop')

        self.title("BenchBot")
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
