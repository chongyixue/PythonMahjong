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

        self.__frame = masterframe
        self.__framename = ""
        if 'framename' in options.keys():
            self.__framename = options['framename']
        self.__image_options(**options,clickable=clickable)
        
        
        self.__button =  tk.Button(
                master=self.__frame,
                text=self.__text,
                image = self.__imagetk,
                compound = self.__compound
        )
        
    def __image_options(self,**options):
        script_dir = os.path.dirname(__file__) 
        image_dir = os.path.join(script_dir,'tileimages')
        self.__fullimagename = os.path.join(image_dir,self.imagename()) 
        self.__clickable = options['clickable']
        compound = "top"
        orientation = 0
        self.__scale = 1
        self.__scale_relative = 0.7
        scale = self.__scale
        if 'orientation' in options.keys():
            if options['orientation'] == 'invert':
                orientation = 180
                scale = self.__scale_relative
            elif options['orientation'] == 'left':
                orientation = -90
                compound = "left"
                scale = self.__scale_relative            
            elif options['orientation'] == 'right':
                orientation = 90
                compound = "right"
                scale = self.__scale_relative
            self.__orientation = orientation
        self.__compound = compound
        
        self.__text = str(self.__tile)
        self.__showtext = True
        
        if 'hidden' in options.keys():
            if options["hidden"] == True:
                self.__showtext = False
                self.__fullimagename = os.path.join(image_dir,'green.jpg')  
                self.__clickable = False
                self.__text = ""
        
        if 'showtext' in options.keys():
            if not options['showtext']:
                self.__text = ""
        
        image = Image.open(self.__fullimagename)
        image = image.rotate(orientation, expand=True)
        image = image.resize([int(s*scale) for s in image.size])
        self.__imagetk = ImageTk.PhotoImage(image)



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
    def __init__(self,tilelist,frame,**options):
        self.__master = frame
        self.__tilelist = tilelist
        self.__orientation = 'upright' 
        self.__framename = ""
        if 'framename' in options.keys():
            self.__framename = options['framename']
        
        if 'orientation' in options.keys():
            self.__orientation = options['orientation']
        pack = tk.LEFT
        if self.__orientation == 'invert':
            pack = tk.RIGHT
        elif self.__orientation == "left":
            pack = tk.TOP
        elif self.__orientation == "right":
            pack = tk.BOTTOM
        self.__pack = pack
        self.packtiles(**options)

    def packtiles(self,**options):
        tblist = []
        buttonlist = []
        tilelist = self.__tilelist
        for i in range(len(tilelist)):
            tb = TileButton(tilelist[i],self.__master,
                            **options)
            tblist.append(tb)
    
        for i in range(len(tilelist)):
            tb = tblist[i]
            button = tb.get_button()
            tile = tb.get_tile()
    
            def handler(event,tile=tile,framename=self.__framename):
                return handle_click(event,tile=tile,framename=framename)
                #return handle_click(event,tile,framename)
    
            button.bind("<Button-1>",handler)
            button.pack(side=self.__pack) 
            buttonlist.append(button)
            self.tblist = tblist
            self.buttonslit = buttonlist



#def handle_click(event,tile, framename):
#    print(tile," from ",framename ," was clicked!")
def handle_click(event,**args):
    print(args['tile']," from ",args['framename']," was clicked!")


window = tk.Tk()
tilelist = [Tiles("dragons",1),Tiles("dragons",1),Tiles("dragons",1),
          Tiles("dragons",2),Tiles("dragons",2),Tiles("dragons",2),
          Tiles("dragons",3),Tiles("dragons",3),Tiles("dragons",3),
          Tiles("winds",1),Tiles("winds",1),Tiles("winds",1),
          Tiles("winds",2),Tiles("winds",2)]


frame = tk.Frame(master=window)
frame2 = tk.Frame(master=window)
frame3 = tk.Frame(master=window)
frame4 = tk.Frame(master=window)

frame.grid(row=2,column=1)
frame2.grid(row=1,column=2)
frame3.grid(row=0,column=1)
frame4.grid(row=1,column=0)


bar = BarOfTiles(tilelist,frame,framename = 'player') 
bar3 = BarOfTiles(tilelist,frame3,framename = 'across',
                  orientation='invert',hidden=True)  
bar2 = BarOfTiles(tilelist,frame2, framename = 'right',
                  orientation='right',hidden=True)  
bar4 = BarOfTiles(tilelist,frame4,framename = 'left',
                  orientation='left',hidden=True)  




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






