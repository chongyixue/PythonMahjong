# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 15:24:20 2021

@author: chong
"""


import os
import tkinter as tk
from mahjong_components import Tiles
from PIL import Image, ImageTk
from mahjong_components import *
from mahjong_players import *
from mahjong_rules import *
from mahjong_game_class import *

class TileButton():
    def __init__(self,tile,masterframe,clickable=True,**options):
        # if tile== None: will print green tile
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
        if self.__tile:
            self.__text = str(self.__tile)
        else:
            self.__text = " "
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
        if not tile:
            return "green.jpg"
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

        elif tile.bonus: # "bonus tile"
            if tile.family == "seasons":
                name = "seas" + str(tile.number)
            else: # "flowers"
                name = "flower" + str(tile.number)
        return name + ".jpg"



## obiously class of baroftiles not working
        
class BarOfTiles():
    def __init__(self,tilelist,frame,**options):
        self.__master = frame
        self.__tilelist = []
        self.__orientation = 'upright' 
        self.__framename = ""
        self.options = options
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
        self.packtiles(tilelist,**options)

    def packtiles(self,tilelist,**options):
        self.tblist = []
        self.buttonlist = []        
        for i in range(len(tilelist)):
            self.addtile(tilelist[i])
        
    def get_tilelist(self):
        return self.__tilelist
    
    def addtile(self,tile):
        self.__tilelist.append(tile)
        tboptions = {k:v for k,v in self.options.items()}
        tboptions['hidden'] = False
        tb = TileButton(tile,self.__master,**tboptions)
        self.tblist.append(tb)
        button = tb.get_button()
        #tile,framename,button,tb,baroftile
        args = {'tile':tile,'framename':self.__framename,'button':button,
                'tb':tb,'baroftile':self}
        def handler(event,args=args):
            return handle_click(event,**args)
        button.bind("<Button-1>",handler)
        button.pack(side=self.__pack) 
        self.buttonlist.append(button)
        
    def removetile(self,i):
        if type(i) == int:
            self.tblist.pop(i)
            button = self.buttonlist.pop(i)
            button.destroy()
            self.__tilelist.pop(i)
        else: # i is a tile
            for (j,tile) in enumerate(self.__tilelist):
                if i == tile:
                    self.removetile(j)
                    break
    def removetiles(self,tilelist):
        for tile in tilelist:
            self.removetile(tile)
                
 

#def handle_click(event,tile, framename):
#    print(tile," from ",framename ," was clicked!")
def handle_click(event,**args):
    # **args: tile,framename,button,tb,baroftile
    print(args['tile']," from ",args['framename']," was clicked!")


# gamemanager.pass_info_to_player(self,n):
# return the state of affairs: 
# ([previous hand, own hand, next hand, next next hand],
#        discardedpile, ntilesleft,gamelog)

class MahjongTable():
    def __init__(self, window, playernumber,
                 handlist, discardpile, ntilesleft, gamelog, **options):
        self.__playernumber = playernumber
        self.__nplayers = 3 # don't worry, will add one down there
        self.__previoushand = handlist[0]
        self.__ownhand = handlist[1]
        self.__nexthand = handlist[2]
        self.__handlist = handlist
        
        if len(handlist) == 4:
            self.__nextnexthand = handlist[3]
            self.__nplayers += 1
            
        self.__discardpile = discardpile
        self.__ntilesleft = ntilesleft
        self.__gamelog = gamelog
        self.__window = window
        self.__initialize_table()
        
    def __initialize_table(self):
        w = self.__window
        n = self.__nplayers
        # the cycle goes leftplayer, player, rightplayer, across
        self.__hiddenframes = [tk.Frame(master=w) for _ in range(n)]
        self.__displayframes = [tk.Frame(master=w) for _ in range(n)]
        self.__discardframe = tk.Frame(master=w)
        hiddentuples = [(2,0),(4,2),(2,4),(0,2)]
        displaytuples = [(2,1),(3,2),(2,3),(1,2)]
        for k,frame in enumerate(self.__hiddenframes):
            (i,j) = hiddentuples[k]
            frame.grid(row=i,column=j)
            frame2 = self.__displayframes[k]
            (i,j) = displaytuples[k]
            frame2.grid(row=i,column=j)
        
        barpairslist = []
        for i in range(n):
            barpairtuple = self.__populate_barpair(i)
            barpairslist.append(barpairtuple)
        self.__barpairslist = barpairslist
        
    
    def get_barpairslist(self):
        return self.__barpairslist
    
    def __populate_barpair(self,playerindex):
        hiddenornot = True
        if playerindex == 1:
            hiddenornot = False
        orientations = ['left','player','right','invert']
        orientation = orientations[playerindex]
        hiddenframe = self.__hiddenframes[playerindex]
        displayframe = self.__displayframes[playerindex]
        hand = self.__handlist[playerindex]
        hiddenbar = BarOfTiles(hand.hidden,hiddenframe,
                               framename = orientation+"_hidden",
                               hidden = hiddenornot,
                               orientation = orientation
                    )
        displaybar = BarOfTiles(
                hand.bonus + hand.shown,displayframe,
                framename = orientation+"_display",
                orientation = orientation
                    )

        return (hiddenbar,displaybar)     
    
    
    def updatehand(self,relativeplayer,newhand):
        ## important! self.__handlist is not always updated
        self.__handlist[relativeplayer] = newhand
        newhidden = newhand.hidden 
        newdisplay = newhand.shown + newhand.bonus
        
        oldhiddenbar,olddisplaybar = self.__barpairslist[relativeplayer]
        oldhiddentiles = oldhiddenbar.get_tilelist()[:]
        olddisplaytiles = olddisplaybar.get_tilelist()[:]
        
        # hidden        
        (add,sub) = Helperfunctions.tiledifference(oldhiddentiles,newhidden)
        print("to add: ",add)
        print("to subtrat: ",sub)

        for t in add:
            self.addtile(relativeplayer,t,location='hidden')
        for t in sub:
            self.removetile(relativeplayer,t,location='hidden')
        
        # display 
        (add,sub) = Helperfunctions.tiledifference(
                                olddisplaytiles,newdisplay
                                )
        for t in add:
            self.addtile(relativeplayer,t,location='display')
        for t in sub:
            self.removetile(relativeplayer,t,location='display')
        

    
    # this one is to test adding a tile. Will be modified to be more generic
    def addtile(self,relativeplayer,tile,location='hidden'):
        # not ideal coding: have to manually add/remove tile from 
        # mahjong table self.__handlist instead of getting from baroftiles
        # because baroftiles does not distinguish between shown and bonus
        hiddenordisplay = 0
        if location != 'hidden':
            hiddenordisplay = 1
           
        baroftiles = self.__barpairslist[relativeplayer][hiddenordisplay]
        baroftiles.addtile(tile)
        
    def removetile(self,relativeplayer,index,location='hidden'):
        hiddenordisplay = 0
        if location != 'hidden':
            hiddenordisplay = 1
                
        baroftiles = self.__barpairslist[relativeplayer][hiddenordisplay]
        baroftiles.removetile(index)
        
        
        

class Helperfunctions():
    def tiledifference(oldlist,newlist):
        # returns tuple ([add to oldlist],[subtract from old list])
        # eg. oldlist = [1,2,3,4,5], newlist = [2,3,4,5,6]
        # return: ([6],[1])
        old = sorted(oldlist, key=lambda x: (x is None, x))
        new = sorted(newlist, key=lambda x: (x is None, x))
        p1, p2 = 0,0
        subtract = []
        add = []
        while True:
            if p1 >= len(old) or p2 >= len(new):
                break
            
            if old[p1] == new[p2]:
                p1 += 1
                p2 += 1
                
            elif old[p1] < new[p2]:
                subtract.append(old[p1])
                p1 += 1
                
            else:
                add.append(new[p2])
                p2 += 1
        if old[p1:]:
            subtract += old[p1:]
        if new[p2:]:
            add += new[p2:]
        return (add,subtract)




        
#a = [Tiles('bamboo',3),Tiles('dragons',2),Tiles('winds',1)]
#b = [Tiles('bamboo',3),Tiles('dragons',3),Tiles('winds',1),Tiles('dots',1),None]
#add, sub = Helperfunctions.tiledifference(a,b)    
#print("add: ",add)
#print("sub: ",sub)


try:
    print(startmarker)
    print("reuse game")
except:
    playerinstancelist = [Player(0),Player(1),
                      Player(2),Player(3)] 
    game = GameManager(playerinstancelist=playerinstancelist)
    game.startgame()     

# gamemanager.pass_info_to_player(self,n):
# return the state of affairs: 
# ([previous hand, own hand, next hand, next next hand],
#        discardedpile, ntilesleft,gamelog)


    (handlist,discardpile, ntilesleft,gamelog) = game.pass_info_to_player(2)
    startmarker = 1
   


window = tk.Tk()

mahjongtable = MahjongTable(window, 2,
                 handlist[:], discardpile, ntilesleft, gamelog)

tk.mainloop()

window = tk.Tk()

mahjongtable = MahjongTable(window, 2,
                handlist[:], discardpile, ntilesleft, gamelog)

#mahjongtable.removetile(1)

mahjongtable.updatehand(1,handlist[2])
mahjongtable.updatehand(2,handlist[1])
mahjongtable.addtile(1,Tiles("joker",0))
mahjongtable.removetile(1,8)
tk.mainloop()
    
"""
### sample table taht works, encapsulated in a class, need to add functions now
###
  
playerinstancelist = [Player(0),Player(1),
                      Player(2),Player(3)] 
game = GameManager(playerinstancelist=playerinstancelist)
game.startgame()     

# gamemanager.pass_info_to_player(self,n):
# return the state of affairs: 
# ([previous hand, own hand, next hand, next next hand],
#        discardedpile, ntilesleft,gamelog)
(handlist,discardpile, ntilesleft,gamelog) = game.pass_info_to_player(2)



window = tk.Tk()
mahjongtable = MahjongTable(window, 
                 handlist, discardpile, ntilesleft, gamelog)


tk.mainloop()




### sample table that works but not yet encapsulated in a class
###

#def handle_click(event,tile, framename):
#    print(tile," from ",framename ," was clicked!")
def handle_click(event,**args):
    print(args['tile']," from ",args['framename']," was clicked!")
        

window = tk.Tk()
tilelist = [None,Tiles("dragons",1),Tiles("dragons",1),
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






