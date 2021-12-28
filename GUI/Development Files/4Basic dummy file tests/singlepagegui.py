import sys
import os
from tkinter import *

window = Tk()
window.title("Benchbot App")
window.geometry("440x342")

lbl1 = Label(window, text="Continous Movements")
lbl1.grid(column=2, row=0)

def forwardc():
    os.system("python3 moveContForward.py")
def backwardc():
    os.system("python3 moveContBackward.py")
	
btn1 = Button(window, text="^", fg="black", command=forwardc)
btn1.grid(column=5, row=10)

btn2 = Button(window, text="v", fg="black", command=backwardc)
btn2.grid(column=5, row=20)


lbl2 = Label(window, text="Relative Movements")
lbl2.grid(column=2, row=50)

def forwardr():
    os.system("python3 moveRelativeForward.py")
def backwardr():
    os.system("python3 moveRelativeBackward.py")

btn3 = Button(window, text="^", fg="black", command=forwardr)
btn3.grid(column=5, row=60)

btn4 = Button(window, text="v", fg="black", command=backwardr)
btn4.grid(column=5, row=70)


window.mainloop()