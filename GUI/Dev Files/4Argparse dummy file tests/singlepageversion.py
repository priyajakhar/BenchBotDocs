import sys
import os
from tkinter import *

window = Tk()
window.title("Benchbot App")
window.geometry("440x342")

lbl1 = Label(window, text="Continous Movements")
lbl1.grid(column=0, row=0)

lbl1s = Label(window, text="Enter speed")
lbl1s.grid(column=0, row=5)
speed = Entry(window,width=3)
speed.grid(column=1, row=5)

lbl1d = Label(window, text="Enter duration")
lbl1d.grid(column=0, row=10)
duration = Entry(window,width=3)
duration.grid(column=1, row=10)

def forwardc():
    comm = "python3 moveContForward.py -s " + speed.get() + " -t " + duration.get()
    os.system(comm)
def backwardc():
    comm = "python3 moveContBackward.py -s " + speed.get() + " -t " + duration.get()
    os.system(comm)
	
btn1 = Button(window, text="^", fg="black", command=forwardc)
btn1.grid(column=1, row=50)

btn2 = Button(window, text="v", fg="black", command=backwardc)
btn2.grid(column=1, row=60)

window.mainloop()