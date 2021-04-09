# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 23:39:04 2021

@author: chong
"""

import tkinter as tk

"""
window = tk.Tk()

label = tk.Label(
        text="Mahjong",
        foreground = "#EC3939",
        background = "black",
        width = 40,
        height = 10
)
label.pack()

button = tk.Button(text="dummy")
button.pack()

entry = tk.Entry(fg = "yellow", bg = "blue",width = 50)
entry.pack()

text_box = tk.Text()
text_box.pack()
window.mainloop()


window2 = tk.Tk()
label2 = tk.Label(text="SECOND window!")
label2.pack()

window.mainloop()





window = tk.Tk()

border_effects = {
    "flat": tk.FLAT,
    "sunken": tk.SUNKEN,
    "raised": tk.RAISED,
    "groove": tk.GROOVE,
    "ridge": tk.RIDGE,
}

frame_a = tk.Frame()
frame_b = tk.Frame()

label_a = tk.Label(master=frame_a, text = "this is Frame A")
label_a.pack()

label_b = tk.Label(master=frame_b, text = "this is Frame B")
label_b.pack()

frame_a.pack()
frame_b.pack()

for relief_name, relief in border_effects.items():
    frame = tk.Frame(master=window, relief=relief, borderwidth=5)
    frame.pack(side=tk.LEFT)
    label = tk.Label(master=frame, text=relief_name)
    label.pack()

window.mainloop()



"""

import os
from PIL import Image, ImageTk

window = tk.Tk()

n = 5
middle = n//2
minsize_sides = 24
minsize_middle = minsize_sides*20

def increase():
    value = int(label["text"])
    label["text"] = f"{value+1}"
    
def decrease():
    value = int(label["text"])
    label["text"] = f"{value-1}"

framels = []
labells = []
colors = ["#75BF24","#BF5724","#33BF24","#21DEC8","#214BDE",
          "#9721DE","#9721DE","#DE21BB","#DE2166"]
for i in range(n):
    if i != middle:
        window.columnconfigure(i, weight=0,minsize=minsize_sides)
        window.rowconfigure(i, weight=0,minsize=minsize_sides)
    else:
        window.columnconfigure(i, weight=1,minsize=minsize_middle)
        window.rowconfigure(i, weight=1,minsize=minsize_middle)
    
    for j in range(n):
        frame = tk.Frame(
                master=window,
                relief=tk.RAISED,
                borderwidth=3,
                bg = colors[1]
        )
        framels.append(frame)
        
        frame.grid(row=i, column=j, padx=5, pady=5,sticky="nesw")
        
        if len(framels) == 5:
            continue
        
        label = tk.Label(
                master=frame,
                text=f"Row {i}\nColumn{j}",
                bg = colors[1]
                )
        label2 = tk.Label(master=frame,text="duplicate",bg = colors[1])
        label.pack(side=tk.LEFT,padx=5, pady=5)
        label2.pack(side=tk.BOTTOM)
        labells.append(label)

middleframe = framels[n**2//2]
       

label = labells[n**2//2]


def handle_keypress(event):
    print(event.char)
    
def handle_click(event):
    print("The button was clicked!")
    increase()
    

script_dir = os.path.dirname(__file__) 
image_dir = os.path.join(script_dir,'tileimages')
imgname1 = 'bb.png'
imgname2 = 'bb.jpg'
imgname3 = 'duo.png'
#photo = tk.PhotoImage(file = os.path.join(image_dir,'bb.png'))
## note that if it shows image pyimage[number] doesn't exist, 
## restart kernel.
## PIL allows both jpg and png; tk.PhotoImage only png.


photo = Image.open(os.path.join(image_dir,imgname2))
phototk = ImageTk.PhotoImage(photo)

duo = Image.open(os.path.join(image_dir,imgname3))
duotk = ImageTk.PhotoImage(duo)

button = tk.Button(
        master=middleframe,
        image = duotk,
        text="add one")#,
        #compound = "left")
button.pack(fill=tk.BOTH) 


window.bind("<Key>",handle_keypress)
button.bind("<Button-1>",handle_click)

label["text"] = "0"

button2 = tk.Button(
        master=middleframe,
        text="minus one",
        command=decrease,
        image = phototk,
        compound = "top"
        )
button2.pack(fill=tk.BOTH)


def addbutton():
    bt = tk.Button(master=f,text='added')
    bt.grid(row = 4,column=4)

f = framels[4]
b = tk.Button(master=f, text='1')
b2 = tk.Button(master=f, text='2')
b3 = tk.Button(master=f, text='3')
b4 = tk.Button(master=f, text='4')
b5 = tk.Button(master=f, text='5')
b6 = tk.Button(master=f, text='6')
b7 = tk.Button(master=f, text='7',command=addbutton)
b.grid(row=0,column=0)
b2.grid(row=0,column=1)
b3.grid(row=0,column=2)
b4.grid(row=1,column=0)
b5.grid(row=1,column=1)
b6.grid(row=1,column=2)
b7.grid(row=2,column=0)


window.mainloop()
        

"""
w = tk.Tk()
b = tk.Button(master=w, text='1')
b2 = tk.Button(master=w, text='2')
b3 = tk.Button(master=w, text='3')
b4 = tk.Button(master=w, text='4')
b5 = tk.Button(master=w, text='5')
b6 = tk.Button(master=w, text='6')
b7 = tk.Button(master=w, text='7')



b.pack(side = tk.TOP)
b2.pack(side=tk.TOP)
b3.pack(side = tk.LEFT)
b4.pack(side = tk.LEFT)
b5.pack(side = tk.TOP)
b6.pack(side = tk.TOP)
b7.pack(side = tk.TOP)


window.mainloop()
"""

















