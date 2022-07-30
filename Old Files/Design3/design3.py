import time, tkinter as tk, threading
from tkinter import *

global stop_exec

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.backGroundImage=PhotoImage(file="bg.png")
        self.backGroundImageLabel=Label(self,image=self.backGroundImage)
        self.backGroundImageLabel.place(x=0,y=0)
        
        def start():
            print('Start it boy!!')
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
        self.geometry("960x495")
        self.resizable(False, False)

        self.start_btn = PhotoImage(file="start.png")
        Button(self, image=self.start_btn, borderwidth=0, bg='white', command=lambda:threading.Thread(target=start).start()).place(x=530,y=373)

        def validate(P):
            if str.isdigit(P) or P == "":
                return True
            else:
                return False
        vcmd = self.register(validate)

        rdist = Entry(self, borderwidth=0, validate='key', validatecommand=(vcmd, '%P'), width=5, justify='right')
        rdist.insert(END, '10')
        rdist.place(x=820,y=150)
        
        cdist = Entry(self, borderwidth=0, validate='key', validatecommand=(vcmd, '%P'), width=5, justify='right')
        cdist.insert(END, '10')
        cdist.place(x=820,y=175)

        rtotal = Entry(self, borderwidth=0, validate='key', validatecommand=(vcmd, '%P'), width=5, justify='right')
        rtotal.insert(END, '1')
        rtotal.place(x=820,y=230)

        ctotal = Entry(self, borderwidth=0, validate='key', validatecommand=(vcmd, '%P'), width=5, justify='right')
        ctotal.insert(END, '1')
        ctotal.place(x=820,y=255)

        self.stop_btn = PhotoImage(file="stop.png")
        Button(self, image=self.stop_btn, borderwidth=0, bg='white', command=lambda:threading.Thread(target=stop).start()).place(x=740,y=373)
        
if __name__ == "__main__":
    root = Window()
    root.iconphoto(False, tk.PhotoImage(file='newimg.png'))
    root.mainloop()
