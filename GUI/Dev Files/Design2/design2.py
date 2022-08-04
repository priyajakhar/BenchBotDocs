import time, tkinter as tk, threading
from tkinter import *

global stop_exec

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.backGroundImage=PhotoImage(file="back.png")
        self.backGroundImageLabel=Label(self,image=self.backGroundImage)
        self.backGroundImageLabel.place(x=0,y=0)
        
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
        self.geometry("468x444")
        self.resizable(False, False)

        self.start_btn = PhotoImage(file="start.png")
        Button(self, image=self.start_btn, borderwidth=0, command=start).place(x=170,y=627)
        Label(self, text="Data Acquisition", font="Playfair 28 bold", bg='#80E7DF').place(x=150,y=175)

        def validate(P):
            if str.isdigit(P) or P == "":
                return True
            else:
                return False
        vcmd = self.register(validate)

        Label(self, text="Distance between rows (cm)", font="Times 20 bold", bg='#80E7DF').place(x=175,y=250)
        rdist = Entry(self, borderwidth=0, validate='key', validatecommand=(vcmd, '%P'), width=5, justify='right')
        rdist.insert(END, '10')
        rdist.place(x=450,y=250)
        
        Label(self, text="Distance between columns (cm)", font="Times 20 bold", bg='#80E7DF').place(x=175,y=275)
        cdist = Entry(self, borderwidth=0, validate='key', validatecommand=(vcmd, '%P'), width=5, justify='right')
        cdist.insert(END, '10')
        cdist.place(x=450,y=275)

        Label(self, text="Row count", font="Times 20 bold", bg='#80E7DF').place(x=175,y=300)
        rtotal = Entry(self, borderwidth=0, validate='key', validatecommand=(vcmd, '%P'), width=5, justify='right')
        rtotal.insert(END, '1')
        rtotal.place(x=450,y=300)

        Label(self, text="Column count", font="Times 20 bold", bg='#80E7DF').place(x=175,y=325)
        ctotal = Entry(self, borderwidth=0, validate='key', validatecommand=(vcmd, '%P'), width=5, justify='right')
        ctotal.insert(END, '1')
        ctotal.place(x=450,y=325)

        Button(self, text=" Begin Data Collection  ", bg="white", fg="black", command=lambda:threading.Thread(target=startcollec).start()).place(x=450,y=220)
        
        self.stop_btn = PhotoImage(file="stop.png")
        Button(self, image=self.stop_btn, borderwidth=0, command=lambda:threading.Thread(target=stop).start()).place(x=495,y=630)
        
        
        
if __name__ == "__main__":
    root = Window()
    root.iconphoto(False, tk.PhotoImage(file='icn.png'))
    root.mainloop()
