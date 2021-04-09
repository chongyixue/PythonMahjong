# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 15:24:20 2021

@author: chong
"""


import os
import time
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
                compound = self.__compound,
        )
        
    def __image_options(self,**options):
        script_dir = os.path.dirname(__file__) 
        image_dir = os.path.join(script_dir,'tileimages')
        self.__fullimagename = os.path.join(image_dir,self.imagename()) 
        self.__clickable = options['clickable']
        compound = "top"
        orientation = 0
        self.__scale = 1
        if 'scale' in options.keys():
            self.__scale = options['scale']
        
        self.__scale_relative = 0.6
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
                
    def disableTileClick(self):
        for tb in self.tblist:
            tb.get_button().unbind("<Button-1>")
            
    def enableTileClick(self,handle_click,**extra):
        for tb in self.tblist:
            args = {'tile':tb.get_tile(),'framename':self.__framename,
                    'button':tb.get_button(),
                    'tb':tb,'baroftile':self}
            for key,val in extra.items():
                args[key] = val
            def handler(event,args=args):
                return handle_click(event,**args)
            tb.get_button().bind("<Button-1>",handler)




# gamemanager.pass_info_to_player(self,n):
# return the state of affairs: 
# ([previous hand, own hand, next hand, next next hand],
#        discardedpile, ntilesleft,gamelog)

class MahjongTable():
    def __init__(self, gameGUI, window, playernumber,
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
        self.__discardpile_cols = 15
        self.__discardpile_tb = []
        
        self.__ntilesleft = ntilesleft
        self.__gamelog = gamelog
        self.__window = window
        self.__initialize_table()
        
        self.gameGUI = gameGUI
        
        
        self.tablestate = None  # "all in tbe perspective of GUI player"
                                # "discard","action","arrange"
        self.tileclicks_n = 0  # if discard, this will be 1, if pong, 2 and so on
        self.tbstore = []    # temporarily store tilebuttons
        
        
        self.handlist = None
        self.newdiscardpile = None
        self.ntilesleft = None
        self.gamelog = None
        
        
    def __initialize_table(self):
        w = self.__window
        n = self.__nplayers
        # the cycle goes leftplayer, player, rightplayer, across
        self.__hiddenframes = [tk.Frame(master=w) for _ in range(n)]
        self.__displayframes = [tk.Frame(master=w) for _ in range(n)]
        self.__discardframe = tk.Frame(master=w)
        self.__actionframe = tk.Frame(master=w)
        self.__populate_buttons()
        
        self.__discardframe.grid(row = 2,column=2)
        
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
        
        self.__update_discardpile(self.__discardpile)
    
    def __populate_buttons(self):
        self.__actionframe.grid(row=3,column=3)
        self.btn_action = tk.Button(master = self.__actionframe,
                                      text="take in / pong / gong")
        def action_handler(event):
            self.action()
        
        self.btn_action.bind("<Button-1>", action_handler)
        
        def draw_handler(event):
            self.action_click(mahjongtable=self,action="draw")
        #def nothing_handler(event):
        #    self.action_click(mahjongtable=self,
        #                      action="nothing",
        #                      gameGUI = self.gameGUI)
            
        self.btn_draw = tk.Button(master = self.__actionframe,
                                    text="draw")
        self.btn_draw.bind("<Button-1>",draw_handler)
        self.btn_nothing = tk.Button(master = self.__actionframe,
                                     text = "do nothing")
        self.bind_nothing_button()
        #
        #self.btn_nothing.bind("<Button-1>",nothing_handler)

        self.btn_action.pack(side = tk.TOP)
        self.btn_draw.pack(side = tk.LEFT)
        self.btn_nothing.pack(side=tk.LEFT)
        
    def bind_nothing_button(self):
        def nothing_handler(event):
            self.action_click(mahjongtable=self,
                              action="nothing",
                              gameGUI = self.gameGUI)

        self.btn_nothing.bind("<Button-1>",nothing_handler)
        
        
    def get_playernumber(self):
        return self.__playernumber
    
    def action(self):
        if self.tablestate == "discard":
            return

        w2 = tk.Tk()
        
        label = tk.Label(master=w2,text="What action?")
        def eat_handler():
            w2.destroy()
            self.action_click(action='take in')
        def pong_handler():
            w2.destroy()
            self.action_click(action='pong')
        def gong_handler():
            w2.destroy()
            self.action_click(action='gong')
        def win_handler():
            w2.destroy()
            self.action_click(action='win')
        
        
        btn_eat = tk.Button(master=w2,
                            text="take in", 
                            command = eat_handler)
        btn_pong = tk.Button(master=w2,
                            text="pong", 
                            command = pong_handler)
        btn_gong = tk.Button(master=w2,
                            text="gong", 
                            command = gong_handler)
        btn_win = tk.Button(master=w2,
                            text="claim victory", 
                            command = win_handler)
        
        label.pack()
        btn_eat.pack()
        btn_pong.pack()
        btn_gong.pack()
        btn_win.pack()
        w2.mainloop()
    
    def update_table(self):
        handlist = self.handlist
        discardpile = self.newdiscardpile
        self.__update_discardpile(discardpile)
        for i in range(4):
            self.updatehand(i,handlist[i])
        print("updated table!")
        print(self.__discardpile)
    
    
    def get_barpairslist(self):
        return self.__barpairslist
        
    def __update_discardpile(self, newdiscardpile):
        i = 0
        (r,c) = (0,0)
        maxi = max(len(newdiscardpile),len(self.__discardpile))
        master = self.__discardframe

        self.__discardpile = newdiscardpile[:]
        tblist = self.__discardpile_tb
                
        for i in range(maxi):
            if i < len(newdiscardpile):
                if i < len(tblist):
                    print(i)
                    # check so that both consistent
                    if tblist[i].get_tile() != newdiscardpile[i]:
                        (f,n) = newdiscardpile[i].get_tile()
                        tile = Tiles(f,n)
                        self.__discardpile[i] = tile
                        tblist[i].destroy()
                        tblist[i] = TileButton(tile,master,scale=0.7)
                        tblist[i].get_button().grid(row=r,column=c)
                    
                else:
                    # add to discardpile
                    tile = newdiscardpile[i]
                    tb = TileButton(tile,master,scale=0.7)
                    tb.get_button().grid(row = r,column = c)
                    self.__discardpile_tb.append(tb)   
                    
            else:
                # newdiscardpile is shorter, delete from discardpile
                tblist[i].destroy()
            
            c += 1
            if c == self.__discardpile_cols:
                c = 0
                r += 1
        
        tblist[len(newdiscardpile):] = []
        self.__discardpile[len(newdiscardpile):] = []
    
    
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
        #print("to add: ",add)
        #print("to subtrat: ",sub)

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
        
        #print("updated relativeplayer ",relativeplayer)
        #time.sleep(2)
    
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
        
    def disableframe(self,displayornot,index):
        self.__barpairslist[index][displayornot].disableTileClick()
        
    def enableframe(self,displayornot,index,**extra):
        self.__barpairslist[index][displayornot].enableTileClick(self.handle_click,**extra)

    
    def disableall(self):
        print("disabling all")
        for i in range(4):
            for j in range(2):
                self.__barpairslist[i][j].disableTileClick()
   
    def enable_tile_select(self):
        self.enableframe(0,1, discard = 1)
        
    def enable_action(self,*args):
        if "do nothing" in args:
            enable_buttons(self.btn_nothing)
        if "draw" in args:
            enable_buttons(self.btn_draw)
        if "action" in args:
            enable_buttons(self.btn_action)

    def disable_action(self,*args):
        if "do nothing" in args:
            disable_buttons(self.btn_nothing)
        if "draw" in args:
            disable_buttons(self.btn_draw)
        if "action" in args:
            disable_buttons(self.btn_action)
    
    def allow_discard(self,game):
        self.facilitate_tileclicks(n=1,option="discard",game=game)    
        self.disable_action("action","draw","do nothing")
        
    
    def facilitate_tileclicks(self,**args):
        # n = number of tiles expected to be clicked
        # option = discard, or pong, or gong.
        # tb = tb
        # game = game
        
        #self.tbstore = []
        #self.tileclicks_n = n
        #self.enable_tile_select()
        self.tbstore.append(args['tb'])            
        n = args['n']
        
        if n <= len(self.tbstore):
            tblist = self.tbstore
            self.tbstore = []
            indexlist = self.tiles_to_index(self.handlist,tblist)
            decision = args['option']
            args['game'].startgame(decision,*indexlist)
        
        
    
    def action_click(self,**args):
        #mapping = ["nothing", "draw","take in","pong with joker",
        #           "pong","gong","win"]
        gameGUI = None
        if 'gameGUI' in args:    
            gameGUI = args['gameGUI']        
        mahjongtable = self
        if 'handlist' in args:
            handlist = args['handlist']
        print("click")
        # **args: action
        action = args['action']
        if action == 'win':
            disable_buttons(mahjongtable.btn_action)
            print('claim victory')
        elif action == 'pong':
            print('pong')
            
            bindplayerbuttons(self.facilitate_tileclicks,
                              mahjongtable=self,game=gameGUI,
                              option='pong',n=2)
            
            
        elif action == 'gong':
            print('gong')
        elif action == 'take in':
            print('take in')
            bindplayerbuttons(self.facilitate_tileclicks,
                              mahjongtable=self,game=gameGUI,
                              option='take in',n=2)        
        elif action == "draw":
            print('draw')
            
        elif action == "nothing":
            print(self.tablestate)
            # tablestate : arange, discard, action - in the perspective of GUIplayer
            if self.tablestate == None:
                gameGUI.startgame('None')
            elif self.tablestate == "action":
                gameGUI.startgame("nothing")
            
    def tiles_to_index(self,handlist,tblist):
        index = []
        tilelist = handlist[1][0]
        for tb in tblist:
            tile = tb.get_tile()
            for (i,t) in enumerate(tilelist):
                if t == tile and i not in index:
                    index.append(i)
                    break
        return index
            

            
    #def handle_click(event,tile, framename):
    #    print(tile," from ",framename ," was clicked!")
    def handle_click(self,event,**args):
        # **args: tile,framename,button,tb,baroftile
        #print(args['tile']," from ",args['framename']," was clicked!")
    
        if 'destroy' in args.keys():
            args['button'].destroy()
    
        if 'discard' in args.keys():
            discard = args['tile']
            print(discard)
            
        

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



class GUIgame(GameManager):
    def __init__(self, GUIplayernumber,playerinstancelist = [Player(1),Player(2),
                        Player(3),Player(4)],autoarrange = True,**options):
        self.playerlist = playerinstancelist
        self.waittime = 1
        self.everyplayerchoose = None
        self.GUIplayernumber = GUIplayernumber
        super().__init__(playerinstancelist = playerinstancelist,**options)
        
        self.autoarrange = autoarrange
        
        (handlist,discardpile,ntilesleft,gamelog) = self.pass_info_to_player(self.GUIplayernumber)    
        self.w = tk.Tk()
        self.mahjongtable = MahjongTable(self,self.w, self.GUIplayernumber,
                 handlist[:], discardpile, ntilesleft, gamelog)
        #self.mahjongtable.disableall()
        #self.mahjongtable.disable_action("action","draw")
        #self.mahjongtable.enable_action("do nothing")
        self.w.mainloop()
        
    def forGUIplayer(self):
        mahjongtable = self.mahjongtable
        infoforGUIplayer = self.pass_info_to_player(self.GUIplayernumber)
        mahjongtable.handlist = infoforGUIplayer[0]
        mahjongtable.newdiscardpile = infoforGUIplayer[1]
        mahjongtable.ntilesleft = infoforGUIplayer[2]
        mahjongtable.gamelog = infoforGUIplayer[3]
    
    # modify this from the GameManager class
    def startgame(self,decision,*n):
        if decision in [None,"none","nothing","None"]:
            dec = ("nothing",[])
        else:
            dec = (decision,*n)
        #makedecision(self,gamestate,
        #             handlists,discardpile, ntileleft, gamelog):
        # states = ['start','drawn','discard','out of cards','end']
        # gamestate = [states[?], player#]
        # RETURN (decision, n)

        # the only difference here while --> if
        
        quickfix = 0
        while quickfix < 1:
            print(self.state)
            
            if self.autoarrange:
                for hand in self.playerhands:
                    hand.arange()

            if self.state[0] in ["drawn","pong","ate","gong"]: 

                # some player drawn. Ask for decision (which tile to discard)
                if self.state[1] == self.GUIplayernumber:
                    # GUI ask player to click a tile to discard
                    #break # break so that GUI can take over
                    self.mahjongtable.tablestate = "discard"
                    self.forGUIplayer()
                    self.mahjongtable.allow_discard(self)
                    return
                    
                else:
                    time.sleep(self.waittime)
                    self.forGUIplayer()
                    self.mahjongtable.update_table()  
                    
                    playertoact = self.playerlist[self.state[1]]
                    info_forplayer = self.pass_info_to_player(self.state[1])

                    # protection against rogue answers
                    canwin = True
                    chances = 3
                    for _ in range(chances):
                        (decision,*n) = playertoact.makedecision(self.state,*info_forplayer)
                        #print("decision ",decision, "  n=",n)
                        
                        if decision == "win" and canwin:
                            print("self=",self)
                            canwin = self.win(self.state[1])
                            print("canwin=",canwin)
                            self.printstate()
                            #print(canwin)
                            if canwin:
                                break
                        else:
                            canwin = False
                            break

                    if canwin:
                        break
                        
                    # decision = "discard by no choice here"
                    if len(n)==0:
                        i = 0
                    else:
                        i = n[0]
                    if i == None:
                        i = 0
                    self.playerdiscard(i)  
                    self.forGUIplayer()
                    time.sleep(self.waittime)
                    self.mahjongtable.update_table()                    
                    self.mahjongtable.enable_action("action","do nothing")
                    self.mahjongtable.disable_action("draw")
                    return self.startgame(None)
 
            elif self.state[0] == "discard":
                # some player discard a tile. Ask everyone for a decision
                # breaking the logic into 2 parts so that bots and GUI both can choose
                #infoforGUI = self.pass_info_to_player(self.GUIplayernumber)
                self.forGUIplayer()
                
                if self.everyplayerchoose: 
                    print("waiting for GUI player's action choice")
                    self.mahjongtable.disable_action("action","draw","do nothing")
                    
                    if self.state[1] != self.GUIplayernumber:
                        playerindex = (self.GUIplayernumber - self.state[1] - 1)%4
                        self.everyplayerchoose[playerindex]=(dec)
                    print("everyplayerchoose=",self.everyplayerchoose)
                    rankedoptions = self.next_player_moves(*self.everyplayerchoose)
                    self.dotherankedmoves(rankedoptions)
                    self.everyplayerchoose = None
                    time.sleep(self.waittime)
                    self.forGUIplayer()
                    self.mahjongtable.update_table()
                    
                    
                    return self.startgame(None)
                    #return infoforGUI
                
                print("Bots deciding")
                every_player_choose = []
                for i in range(1,self.players):
                    p = self.next_player(i)
                    if p != self.GUIplayernumber:
                        playertoact = self.playerlist[p]
                        info_forplayer = self.pass_info_to_player(p)
                        (decision,*n) = playertoact.makedecision(self.state,*info_forplayer)
                        #print("decision: ",decision, " \n n: ", n)
                        every_player_choose.append([decision,*n])
                    else:
                        every_player_choose.append(None) # GUI will replace the None back in
                        #infoforGUI = self.pass_info_to_player(p)
                # do something so that the GUI will tell player to pick action
                # or wait for some seconds before moving on
                self.everyplayerchoose = every_player_choose
                print("XXXXXXX")
                self.forGUIplayer()
                self.mahjongtable.tablestate = "action"

                bind_button(self.mahjongtable.btn_action,self.mahjongtable.action)
                #bind_button(self.mahjongtable.btn_nothing,self.mahjongtable.action)
                
                return 
                #return infoforGUI
                    
                    

            elif self.state[0] == "out of cards":
                # out of cards
                self.printstate()
                self.goodbye()
                break
            
            elif self.state[0] in ["win", "end"]:
                # end game
                self.printstate()
                self.goodbye()
                break
            
            else:
                print("state ",self.state[0], " not recognized")
                break
            
            
            self.printstate()
            quickfix += 1
    
    def goodbye(self):    
        print("++++++++++++ Hope you enjoyed the game ++++++++++++++++++")
                
        
    #def dotherankedmoves(self,rankedoptions):
    #def dothemove(self,player,choice,*n):   
    #def notifystate(self,special = None): # special = ['pong',3]        
    #def cheat(self,option='almost winning',player=1):
    #def pass_info_to_player(self,n):
    #def printstate(self,printoutstr = True):


## really simple Combination with the game manager


    

    
    
    



    

def genericprint():
    print("this is clicked!")

def disable_buttons(*buttons):
    for button in buttons:
        button.unbind("<Button-1>")
        button["state"] = "disable"
    #print("disabled button(s)")
    
def enable_buttons(*buttons):
    for button in buttons:
        button["state"] = "normal"
    #print("enabled button(s)")

def bindplayerbuttons(func,**args):
    baroftiles = args['mahjongtable'].get_barpairslist()[1][0]
    buttonlist = baroftiles.buttonlist
    for bt in buttonlist:
        bind_button(bt,func,**args)
    
    

def bind_button(button, func, **args):
    button['state'] = "normal"
    button.unbind("<Button-1>")
    def func_handler(event):
        func(**args)
    button.bind("<Button-1>",func_handler)
    print("binded")

game = GUIgame(3)

"""
w = tk.Tk()
game = GameManager([Player(0),Player(1),Player(2),Player(3)])
game.startgame()
(handlist,discardpile,ntilesleft,gamelog) = game.pass_info_to_player(2)  
mahjongtable = MahjongTable(w, 2,
                 handlist[:], discardpile, ntilesleft, gamelog)
mahjongtable.disableall()
#mahjongtable.update_table([Tiles("dragons",2),Tiles("dragons",3)],handlist)
w.mainloop()




### could work, but let us rethink and consolidate most parts back into the
    ### GUIgame class

playerinstancelist = [Player(0),Player(1),
                      Player(2),Player(3)] 
    
guiplayer = 1
game = GUIgame(1,playerinstancelist=playerinstancelist)

window = tk.Tk()

def startgame(window):
    print("start game!")
    window.destroy()
    window = tk.Tk()
    GUIplayer = 2

    (handlist,discardpile, ntilesleft,gamelog) = game.pass_info_to_player(GUIplayer)
    mahjongtable = MahjongTable(window, GUIplayer,
                 handlist[:], discardpile, ntilesleft, gamelog)
    mahjongtable.disableall()
    #mahjongtable.enableframe(0,1)
    continuegame(mahjongtable)
    
    window.mainloop()
    
def continuegame(mahjongtable):
    wait = 1
    
    GUIplayer = mahjongtable.get_playernumber
    infoforGUIplayer = game.startgame(None) 
    if infoforGUIplayer:
        (handlist,discardpile,ntilesleft,gamelog) = infoforGUIplayer
        mahjongtable.update_table(discardpile,handlist)
    # ([previous,ownhand,nexthand,next2hand],
    #            discardpile,ntilesleft,gamelog)
    gamestate = game.state
    disable_buttons(mahjongtable.btn_action,mahjongtable.btn_draw)
            
    if gamestate[1] == GUIplayer:
        if gamestate[0] in  ["drawn","pong","ate","gong"]: 
            # ask user to pick, activate button for function
            mahjongtable.enable_tile_select()
            
            
            #continue
                
        elif gamestate[0] == "discard":
            # user just discarded, he/she should not be able to do anything
            pass
    
    else: # (not GUI player)
        
        if gamestate[0] in  ["drawn","pong","ate","gong"]:
            # wait for 3 seconds?    
            time.sleep(wait)
            
        elif gamestate[0] == "discard":
            print("somebody discarded") 
                
                
                
    if gamestate[0] in ["out of cards","win","end"]:
        game.goodbye()     
    
    
    game.printstate()
    
    
def startgame_handler(event,window = window):
    startgame(window)

btn_start = tk.Button(master=window,text = "start game")
btn_start.bind("<Button-1>",startgame_handler)
btn_start.pack()

tk.mainloop()




#### This looks like a good template to start integrating more


playerinstancelist = [Player(0),GUIplayer(1),
                      Player(2),Player(3)] 
    

game = GUIgame(playerinstancelist=playerinstancelist)

window = tk.Tk()

def startgame(window):
    print("start game!")
    window.destroy()
    window = tk.Tk()
    
    (handlist,discardpile, ntilesleft,gamelog) = game.pass_info_to_player(2)
    mahjongtable = MahjongTable(window, 2,
                 handlist[:], discardpile, ntilesleft, gamelog)
    window.mainloop()
    game.startgame() # modify 
    
    
def startgame_handler(event,window = window):
    startgame(window)

btn_start = tk.Button(master=window,text = "start game")
btn_start.bind("<Button-1>",startgame_handler)
btn_start.pack()

tk.mainloop()





### short function test
        
#a = [Tiles('bamboo',3),Tiles('dragons',2),Tiles('winds',1)]
#b = [Tiles('bamboo',3),Tiles('dragons',3),Tiles('winds',1),Tiles('dots',1),None]
#add, sub = Helperfunctions.tiledifference(a,b)    
#print("add: ",add)
#print("sub: ",sub)



### working sample of updating the hands given a new group.


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






