import sys
import os
from tkinter import *
from tkinter import ttk

window = Tk()
window.title("Benchbot App")
window.geometry("440x342")

tab_control = ttk.Notebook(window)

tab1 = ttk.Frame(tab_control)
tab_control.add(tab1, text='Continous Movements')
tab2 = ttk.Frame(tab_control)
tab_control.add(tab2, text='Relative Movements')

tab_control.pack(expand=1, fill='both')


def forwardc():
    comm = "python3 moveContForward.py -s " + speed.get() + " -t " + duration.get()
    os.system(comm)
def backwardc():
    comm = "python3 moveContBackward.py -s " + speed.get() + " -t " + duration.get()
    os.system(comm)
	
lbl1s = Label(tab1, text="Enter speed")
lbl1s.grid(column=0, row=5)
speed = Entry(tab1,width=3)
speed.grid(column=1, row=5)

lbl1d = Label(tab1, text="Enter duration")
lbl1d.grid(column=0, row=10)
duration = Entry(tab1,width=3)
duration.grid(column=1, row=10)

btn1 = Button(tab1, text="^", fg="black", command=forwardc)
btn1.grid(column=1, row=40)

btn2 = Button(tab1, text="v", fg="black", command=backwardc)
btn2.grid(column=1, row=50)



lbl2d = Label(tab2, text="Enter distance")
lbl2d.grid(column=0, row=5)
distance = Entry(tab2,width=3)
distance.grid(column=1, row=5)

def forwardr():
    comm = "python3 moveRelativeForward.py -d " + distance.get()
    os.system(comm)
def backwardr():
    comm = "python3 moveRelativeBackward.py -d " + distance.get()
    os.system(comm)

btn3 = Button(tab2, text="^", fg="black", command=forwardr)
btn3.grid(column=1, row=40)

btn4 = Button(tab2, text="v", fg="black", command=backwardr)
btn4.grid(column=1, row=50)


window.mainloop()