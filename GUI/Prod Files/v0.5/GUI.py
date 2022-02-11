import sys
import os
from tkinter import *

def start():
    os.system("python start.py")
def forward():
    os.system("python moveRelF.py")
def backward():
    os.system("python moveRelB.py")
def stop():
    os.system("python stop.py")
    
window = Tk()
window.title("Benchbot App")
window.geometry("440x342")

btnstart = Button(window, text="START", bg="green", fg="white", command=start)
btnstart.grid(column=0, row=0)

lbl1 = Label(window, text="Move the bot")
lbl1.grid(column=2, row=1)

btn1 = Button(window, text="  Forward  ", bg="white", fg="black", command=forward)
btn1.grid(column=5, row=3)

btn2 = Button(window, text="Backward", bg="white", fg="black", command=backward)
btn2.grid(column=5, row=5)

btnstop = Button(window, text="STOP", bg="red", fg="white", command=stop)
btnstop.grid(column=0, row=7)

window.mainloop()