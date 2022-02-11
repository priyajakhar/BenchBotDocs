import sys
import os
from tkinter import *
from tkinter import ttk

window = Tk()
window.title("Benchbot App")
window.geometry("440x342")

tab_control = ttk.Notebook(window)

tab1 = ttk.Frame(tab_control)
tab_control.add(tab1, text='First')
lbl1 = Label(tab1, text="Continous Movements")
lbl1.grid(column=0, row=0)

tab2 = ttk.Frame(tab_control)
tab_control.add(tab2, text='Second')
lbl2 = Label(tab2, text="Relative Movements")
lbl2.grid(column=0, row=0)

tab_control.pack(expand=1, fill='both')



def forwardc():
    os.system("python3 moveContForward.py")
def backwardc():
    os.system("python3 moveContBackward.py")
	
btn1 = Button(tab1, text="^", fg="black", command=forwardc)
btn1.grid(column=2, row=10)

btn2 = Button(tab1, text="v", fg="black", command=backwardc)
btn2.grid(column=2, row=20)


def forwardr():
    os.system("python3 moveRelativeForward.py")
def backwardr():
    os.system("python3 moveRelativeBackward.py")

btn3 = Button(tab2, text="^", fg="black", command=forwardr)
btn3.grid(column=2, row=10)

btn4 = Button(tab2, text="v", fg="black", command=backwardr)
btn4.grid(column=2, row=20)


window.mainloop()