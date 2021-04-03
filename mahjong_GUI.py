# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 15:24:20 2021

@author: chong
"""


import os
import tkinter as tk
from mahjong_components import Tiles
from PIL import Image, ImageTk


class TileButton():
    def __init__(self,tile,masterframe,clickable=True,**options):
        self.__tile = tile
        script_dir = os.path.dirname(__file__) 
        image_dir = os.path.join(script_dir,'tileimages')
        self.__fullimagename = os.path.join(image_dir,self.imagename())        
        self.__clickable = clickable
        self.__text = str(tile)
        self.__frame = masterframe
        image = Image.open(self.__fullimagename)
        self.__imagetk = ImageTk.PhotoImage(image)
        self.__button =  tk.Button(
                master=self.__frame,
                text=self.__text,
                image = self.__imagetk,
                compound = "top"
        )

    def get_imagetk(self):
        return self.__imagetk

    def get_tile(self):
        return self.__tile
        
    def get_button(self):
        return self.__button
        """
        return tk.Button(
                master=self.__frame,
                text=self.__text,
                image = self.__imagetk,
                compound = "top"
        )
        """

    def get_fullimagename(self):
        return self.__fullimagename
    
    def get_text(self):
        return self.__text
    
    def get_imagename(self):
        return self.imagename()
    
    def imagename(self):
        tile = self.__tile
        if str(tile) == "Joker":
            name = "joker"
        
        if tile.suits:
            if tile.family == "dots":
                name = "t" + str(tile.number)
            elif tile.family == "bamboo":
                name = "s" + str(tile.number)
            else: #"characters"
                name = "w" + str(tile.number)
                
        elif tile.honors:
            if tile.family == "winds":
                if tile.number == 1:
                    name =  "east"
                elif tile.number == 2:
                    name =  "north"
                elif tile.number == 3:
                    name =  "west"
                else: #4:
                    name =  "south"
            else: #"dragons": 
                if tile.number == 1:
                    name =  "red"
                elif tile.number == 2:
                    name =  "huat"
                else: #3:
                    name =  "bb"

        else: # "bonus tile"
            if tile.family == "seasons":
                name = "seas" + str(tile.number)
            else: # "flowers"
                name = "flower" + str(tile.number)
        return name + ".jpg"



## obiously class of baroftiles not working
        
class BarOfTiles():
    def __init__(self,tilelist,frame):
        self.__master = frame
        self.__tilelist = tilelist
        

    def packtiles(self):
        tblist = []
        buttonlist = []
        tilelist = self.__tilelist
        for i in range(len(tilelist)):
            tb = TileButton(tilelist[i],self.__master)
            tblist.append(tb)
    
        for i in range(len(tilelist)):
            tb = tblist[i]
            button = tb.get_button()
            tile = tb.get_tile()
    
            def handler(event,tile=tile):
                return handle_click(event,tile)
    
            button.bind("<Button-1>",handler)
            button.pack(side=tk.LEFT) 
            buttonlist.append(button)
        return (tblist,buttonlist)



def handle_click(event,tile):
    print(tile," was clicked!")


window = tk.Tk()
tilelist = [Tiles("dragons",1),Tiles("dragons",1),Tiles("dragons",1),
          Tiles("dragons",2),Tiles("dragons",2),Tiles("dragons",2),
          Tiles("dragons",3),Tiles("dragons",3),Tiles("dragons",3),
          Tiles("winds",1),Tiles("winds",1),Tiles("winds",1),
          Tiles("winds",2),Tiles("winds",2)]

frame = tk.Frame(master=window)
frame2 = tk.Frame(master=window)

frame.grid(row=0,column=0)
frame2.grid(row=1,column=1)

bar = BarOfTiles(tilelist,frame)   
bar2 = BarOfTiles(tilelist,frame2)  

tblist = bar.packtiles()
tblist2 = bar2.packtiles()


tk.mainloop()

"""

### sample: working for more 2 bars of tiles
### important! in tkinter if you don't keep some refernece to the PhotoImage object,
### it will be garbage collected and the image will be cleared even if it is
### displayed by a Tkinter widget! keep an extra reference to the image object!    

window = tk.Tk()
tilelist = [Tiles("dragons",1),Tiles("dragons",1),Tiles("dragons",1),
          Tiles("dragons",2),Tiles("dragons",2),Tiles("dragons",2),
          Tiles("dragons",3),Tiles("dragons",3),Tiles("dragons",3),
          Tiles("winds",1),Tiles("winds",1),Tiles("winds",1),
          Tiles("winds",2),Tiles("winds",2)]

frame = tk.Frame(master=window)
frame2 = tk.Frame(master=window)

#frame.pack()

frame.grid(row=0,column=0)
frame2.grid(row=1,column=1)


def handle_click(event,tile):
    print(tile," was clicked!")
    
    

        

def packtiles(tilelist,frame):
    tblist = []
    buttonlist = []
    for i in range(len(tilelist)):
        tb = TileButton(tilelist[i],frame)
        tblist.append(tb)
    
    for i in range(len(tilelist)):
        tb = tblist[i]
        button = tb.get_button()
        tile = tb.get_tile()
    
        def handler(event,tile=tile):
            return handle_click(event,tile)
        
        button.bind("<Button-1>",handler)
        button.pack(side=tk.LEFT)
        
        buttonlist.append(button)
    return tblist  

tblist = packtiles(tilelist,frame)
tblist2 = packtiles(tilelist,frame2)
#packtiles(tilelist,frame2)

tk.mainloop()  







### sample working bar of tiles

tilelist = [Tiles("dragons",1),Tiles("dragons",1),Tiles("dragons",1),
          Tiles("dragons",2),Tiles("dragons",2),Tiles("dragons",2),
          Tiles("dragons",3),Tiles("dragons",3),Tiles("dragons",3),
          Tiles("winds",1),Tiles("winds",1),Tiles("winds",1),
          Tiles("winds",2),Tiles("winds",2)]

def handle_click(event,tile):
    print(tile," was clicked!")

windows = tk.Tk()
frame = tk.Frame(master=windows)
frame.pack()

tblist = []
for i in range(len(tilelist)):
    tb = TileButton(tilelist[i],frame)
    tblist.append(tb)
    
for i in range(len(tilelist)):
    tb = tblist[i]
    button = tb.get_button()
    tile = tb.get_tile()
    
    def handler(event,tile=tile):
        return handle_click(event,tile)
    
    button.bind("<Button-1>",handler)
    button.pack(side=tk.LEFT)    

tk.mainloop()
    
 
#### sample workable button with picture

import os
from PIL import Image, ImageTk

window = tk.Tk()


frame = tk.Frame(master=window)
#frame.grid(row=0, column=0, padx=5, pady=5)#,sticky="nesw")
frame.pack()

script_dir = os.path.dirname(__file__) 
image_dir = os.path.join(script_dir,'tileimages')
imgname3 = 'duo.png'

duo = Image.open(os.path.join(image_dir,imgname3))
duotk = ImageTk.PhotoImage(duo)

button = tk.Button(
        master=frame,
        image = duotk,
        text = "duo",
        compound = "top")
button.pack()#(fill=tk.BOTH) 



window.mainloop()

"""






