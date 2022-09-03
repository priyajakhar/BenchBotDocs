## getting count of files in a directory
import fnmatch, os

def list_files():
    files = fnmatch.filter(os.listdir(dir_path), '*.*')
    count = len(files)
    print('File Count:', count)

dir_path = os.getcwd()+'/images'
os.chdir(dir_path)
list_files()



## testing logic of row update algo
rownums = '1,2,3,5-9'
arr1 = rownums.split(',')
species_row = []
for elmnt in arr1:
    print(elmnt)
    if '-' in elmnt:
        arr2 = [int(e) for e in elmnt.split('-')]
        for val in range(arr2[0], arr2[1]+1):
            species_row.append(val)
    else:
        species_row.append(int(elmnt))
print(species_row)



## code for renaming files in a directory based on row count in the excel sheet
import os, pandas as pd
df  = pd.read_excel('weeds.xlsx')
colvalues = df[['pics to take']].values
i = 0
arr = [None] * colvalues.size
for num in colvalues:
	arr[i] = num[0]
	i = i+1
print(arr)
def main():
	j=0
	k=0
	for count, filename in enumerate(os.listdir("Downloads")):
		pots = arr[j]
		dst = f"Row{j+1} Pot{k+1}.jpg"
		src =f"Downloads/{filename}"
		dst = f"Downloads/{dst}"
		os.rename(src, dst)
		if k<pots-1:
			k = k+1
		else:
			k=0
			j=j+1

if _name_ == '_main_':
	main()




## rename files in a directory
import glob, os, time
def main():    
    os.chdir('Images')
    region = ['NC', 'TX', 'MD']
    t = str(time.time())

    fileList = glob.glob("*.JPG")
    for trueFile in fileList:
        dst = f"{region[0]}_Row1_{t}.JPG"
        src =f"{trueFile}"
        dst =f"New Images/{dst}"
        os.rename(src, dst)
    # fileList = glob.glob("*.ARW")
    # for trueFile in fileList:
        # dst = f"{region[0]}_Row1_{t}.ARW"
        # src =f"{trueFile}"
        # dst =f"New Images/{dst}"
        # os.rename(src, dst)
if __name__ == '__main__':
	main()



## another code to rename files
import shutil, os, datetime # pip3 install pytest-shutil
from datetime import date
def main():
    # today = date.today().strftime("%m/%d/%y")
    # print(today)
    shutil.copy("SpeciesSheet.xlsx", "new.xlsx")
    # name = f"{today}_SpeciesSheet.xlsx"
    # os.rename(f"new.xlsx", f"{name}")
    today = datetime.datetime.today().strftime ('%d-%b-%Y')
    os.rename(r'new.xlsx',r'SpeciesSheet_' + str(today) + '.xlsx')

if __name__ == '__main__':
	main()
    
    
     
## For changing label at click of a button
from tkinter import *

win= Toplevel()
win.title("Rounded Button")
win.geometry("700x300")

def my_command():
   text.config(text= "You have clicked Me...")
click_btn= PhotoImage(file='st.png')
img_label= Label(image=click_btn)
Button(win, image=click_btn,command= my_command,borderwidth=0).pack(pady=30)
text= Label(win, text= "")
text.pack(pady=30)
win.mainloop()



## Code for tkinter multiple pages
import tkinter as tk

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class Page1(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="This is page 1")
       label2 = tk.Label(self, text="This is page 1")
       label.pack(side="top", fill="both", expand=True)
       label2.pack(side="top", fill="both", expand=True)

class Page2(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="This is page 2")
       label.pack(side="top", fill="both", expand=True)

class Page3(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="This is page 3")
       label.pack(side="top", fill="both", expand=True)
       
class Page4(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="This is page 4")
       label.pack(side="top", fill="both", expand=True)

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = Page1(self)
        p2 = Page2(self)
        p3 = Page3(self)
        p4 = Page4(self)

        # buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        # buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p4.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        
        b1 = tk.Button(self, text="Page 1", command=p1.show)
        b2 = tk.Button(self, text="Page 2", command=p2.show)
        b3 = tk.Button(self, text="Page 3", command=p3.show)

        #b1 = tk.Button(buttonframe, text="Page 1", command=p1.show)
        #b2 = tk.Button(buttonframe, text="Page 2", command=p2.show)
        #b3 = tk.Button(buttonframe, text="Page 3", command=p3.show)

        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")

if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x400")
    root.mainloop()