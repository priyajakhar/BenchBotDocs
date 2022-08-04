import sys, os
import tkinter as tk
from tkinter import *

class Window(tk.Tk):
	def __init__(self):
		super().__init__()    
		
		def start():
			os.system("python start.py")
				
		def forward():
			d = dist.get()
			s = sped.get()
			if d == '':
				d = '10'
			else:
				if int(d)>500:
					d = '5000'
				elif int(d)<1:
					d = '10'
				else:
					d=d+'0'
			if s == '':
				s = '10'
			else:
				if int(s)>50:
					s = '500'
				elif int(s)<1:
					s = '10'
				else:
					s=s+'0'
			os.system("python moveRelF.py -d "+d+" -s "+s)
		
		def backward():
			d = dist.get()
			s = sped.get()
			if d == '':
				d = '10'
			else:
				if int(d)>500:
					d = '5000'
				elif int(d)<1:
					d = '10'
				else:
					d=d+'0'
			if s == '':
				s = '10'
			else:
				if int(s)>50:
					s = '500'
				elif int(s)<1:
					s = '10'
				else:
					s=s+'0'
			os.system("python moveRelB.py -d "+d+" -s "+s)
		
		def stop():
			os.system("python stop.py")
		
		self.title("Benchbot App")
		self.geometry("540x242")
		self.resizable(False, False)
		self.iconbitmap('./bb.ico')

		btnstart = Button(self, text="START", bg="green", fg="white", command=start).grid(column=0, row=0)

		heading = Label(self, text="Move the bot").grid(column=1, row=1, sticky=W)

		labeldist = Label(self, text="Distance (in cm)").grid(column=2, row=3, sticky=W)
		def validate(P):
			if str.isdigit(P) or P == "":
				return True
			else:
				return False
		vcmd = self.register(validate)
		dist = Entry(self, validate='key', validatecommand=(vcmd, '%P'), width=5, justify='right')
		dist.insert(END, '10')
		dist.grid(column=3, row=3, sticky=E)
		
		labelspd = Label(self, text="Speed (in cm/rev)").grid(column=2, row=4, sticky=W)
		s = StringVar()
		
		sped = Spinbox(self, from_=10, to=100, width=5, justify='right', textvariable=s, validate='key', validatecommand=(vcmd, '%P'))
		sped.grid(column=3, row=4, sticky=E)
		spbar = Scale(self, from_=10, to=100, orient=HORIZONTAL, showvalue=0, sliderlength=10, variable=s).grid(column=5, row=4)

		btnf = Button(self, text=" Forward  ", bg="white", fg="black", command=forward).grid(column=2, row=5, sticky=E)
		btnb = Button(self, text="Backward", bg="white", fg="black", command=backward).grid(column=2, row=7, sticky=E)

		btnstop = Button(self, text="STOP", bg="red", fg="white", command=stop).grid(column=0, row=9, sticky=SW)
		btnquit = Button(self, text="QUIT", command=self.destroy).grid(column=10, row=9, sticky=SE)

  
if __name__ == "__main__":
	root = Window()
	#root.iconphoto(False, tk.PhotoImage(file='bb.png'))
	root.mainloop()
	