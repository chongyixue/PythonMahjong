# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 09:20:06 2021

@author: chong
"""

import random
import csv
import os

class Tiles:
    
    # family: bamboo, characters, dots, 
    # winds, dragons, seasons ,flowers
    # for winds and dragons, 1,2,3,4,   1,2,3: 
    # E,S,W,N,Red,Green,White
    # optional family: joker, number: 0 for joker
    #suits = ['bamboo','characters','dots']
    #honors = ['winds','dragons']
    #bonus = ['seasons','flowers']

    def __init__(self, family, number):
        (self.suits, self.honors, self.bonus, self.joker) = (False, False, 
                                                            False, False)
        self.family = family
        self.number = number
        if self.family in ['bamboo','characters','dots']:
            self.suits = True
            if self.number > 9 or self.number < 1:
                print("suit number out of range, 1-9 only")
                return
        elif self.family in ['winds','dragons']:
            self.honors = True
        elif self.family in ['seasons','flowers']:
            self.bonus = True
        elif self.family == 'joker':
            self.joker = True
        else:
            print(family + ': invalid family')
            return
            
        self.id = self.absolute_number()    
        
        
    def get_tile(self):
        return (self.family, self.number)
    
    def absolute_number(self):
        # 0- joker, 1-8: seasons, flowers
        # 11 - 17: ESWN,red,green, white
        # 20s, 30s, 40, bamboo, characters, dots
        if self.joker: return 0
        if self.bonus:
            return (self.family == 'flowers')*4 + self.number
        if self.honors:
            return self.number + 10 + (self.family == 'dragons')*4
        if self.suits:
            return (self.family == 'bamboo')*20 + self.number \
                + (self.family == 'characters')*30 \
                + (self.family == 'dots')*40 
                
    def shortname(self):
        if self.joker:
            return 'Joker'
        if self.suits:
            return self.family[0] + str(self.number)
        if self.honors:
            ls = ['E','N','W','S','Red','Green','White']
            return ls[self.id%10 - 1]
        if self.bonus:
            return self.family + str(self.number)
        return
    
    def __repr__(self):
        return self.shortname()
    
    def __eq__(self,other):
        return self.id == other.id
    
    def __sub__(self,other):
        if not self.suits or not other.suits:
            return (1 - 1*(self == other))*100
        if self.family != other.family:
            return 100
        return self.id - other.id
    def __lt__(self,other):
        return self.id < other.id
    def __gt__(self,other):
        return self.id > other.id
        
class Rules():
    def ispair(*tiles):
        if len(tiles) != 2:
            return False
        if tiles[0]-tiles[1] == 0:
            return True
        return False
    
    def istriplet_identical(*tiles):
        if len(tiles) != 3:
            return False
        if tiles[0]-tiles[1]==0 and tiles[2]-tiles[1]==0:
            return True
        return False
    
    def istriplet_distinct(*tiles):
        if len(tiles) != 3:
            return False
        c1 = tiles[1] - tiles[0]
        c2 = tiles[1]-tiles[2]
        if (c1,c2) in [(1,-1),(2,1),(-1,-2),(1,2),(-2,-1),(-1,1)]: 
            return True
        return False
    
    def isquadruplet(*tiles):
        if len(tiles) != 4:
            return False
        return tiles[0]-tiles[1]==0 and tiles[2]-tiles[3]==0 \
            and tiles[1]-tiles[2]==0
    
    def istriplet(*tiles):
        return Rules.istriplet_identical(*tiles) \
            or Rules.istriplet_distinct(*tiles)
    
    def isgroup(*tiles):
        return Rules.istriplet(*tiles) or Rules.isquadruplet(*tiles)
    
    def nearby(tilelist,index):
        for (i,tile) in enumerate(tilelist):
            if i != index:
                if abs(tilelist[index] - tile) < 2:
                    return True
        return False
    
    def relatable_to_hand(tile,hand,dist=2):
        count = 0
        for t in hand.hidden:
            if abs(t-tile)<=dist:
                count += 1
        return count
    
    def nsame(tile,hand):
        count = 0
        ls = []
        for (i, t) in enumerate(hand.hidden):
            if t==tile:
                count += 1
                ls.append(i)
        return (count,ls)

    def can_form_group(tile, hand):
        # return (true/false, [possible indices],[possible groups])
        # eg. (True, [[2,3],[3,5]],[[b2,b3,b4],[b3,b4,b5]])
        l = len(hand.hidden)
        possible_indices = []
        possible_groups = []
        
        (count,indexls) = Rules.nsame(tile,hand)
        
        # identical and quad
        if count > 2:
            possible_indices.add([tile]+[hand.hidden[i] for i in indexls[0:3]])
            possible_groups.add([i for i in indexls[0:3]])
        if count > 1:
            possible_indices.add([tile]+[hand.hidden[i] for i in indexls[0:2]])
            possible_groups.add([i for i in indexls[0:2]])            
        
        for i in range(l-1):
            for j in range(i+1,1):
                three = sorted([hand.hidden[i],
                                hand.hidden[j],tile])
                if three not in possible_groups:
                    if Rules.istriplet_distinct(*three):
                        possible_groups.append(three)
                        possible_groups.append([i,j])
    
    def can(action,foreigntile,hand,*n):
        group = [foreigntile] + [hand.hidden[i] for i in n]
        if action in ["eat","take in"]:
            return Rules.istriplet(*group)
        if action in ["pong"]:
            return Rules.istriplet_identical(*group)
        if action in ["gong"]:
            return Rules.isquadruplet(*group)
        return False
        
        
        
    
    
    def iswinning(tilelist, eye=True): 
        # might be confusing. eye means will need an eye from this tilelist
        # return (True/False, winning type, grouping)
        l = len(tilelist)
        if l < 2:
            return (False,None,None)
        if l == 2: 
            if eye==True:
                return (tilelist[0]==tilelist[1],None,[tilelist])
            
            return False
        if l == 3:
            if eye == True:
                return (False,None,None)
            return (Rules.isgroup(*tilelist),None,[tilelist])
        if l == 4:
            if eye == True:
                return (False,None,None)
            return (Rules.isquadruplet(*tilelist),None,[tilelist])
        
        
        # 1. check for special case
        if l==13:
            if sorted(tilelist) == sorted([Tiles('winds',1),Tiles('winds',2),
                      Tiles('winds',3),Tiles('winds',4),Tiles('dragons',1),
                      Tiles('dragons',2),Tiles('dragons',3), Tiles('bamboo',1),
                      Tiles('bamboo',9), Tiles('characters',1), 
                      Tiles('characters',9),Tiles('dots',1), Tiles('dots',9)]):
                return (True,'13orphans',[tilelist])
        
        # eliminate those that are not winning hands
        for i in range(l):
            if Rules.nearby(tilelist,i) == False:
                return (False,None,None)
        
        tl2 = sorted(tilelist)
        
        # make eye, then iterate
        if eye:
            for i in range(l-1):
                for j in range(i+1,l):
                    if tl2[i] == tl2[j]:
                        therest = Rules.iswinning(tl2[0:i]+tl2[i+1:j]+tl2[j+1:],
                                                  eye=False)
                        if therest[0]:
                            return (True,therest[1],
                                    therest[2]+[[tl2[i],tl2[j]]])
            return (False,None,None)
        
        
        # triplet then iterate
        for i in range(l-2):
            for j in range(i+1,l-1):
                for k in range(j+1,l):
                    if Rules.istriplet(tl2[i],tl2[j],tl2[k]) == True:
                        therest = Rules.iswinning(tl2[0:i]+tl2[i+1:j]
                                    +tl2[j+1:k]+tl2[k+1:],eye=False)
                        if therest[0] == True:
                            return (True, therest[1],
                                     therest[2]+[[tl2[i],tl2[j],tl2[k]]])
        
        # unlikely event that quadruplet exists
        for i in range(l-3):
            for j in range(i+1,l-2):
                for k in range(j+1,l-1):
                    for m in range(k+1,l):
                        if Rules.isgroup(tl2[i],tl2[j],tl2[k],tl2[k])==True:
                            therest = Rules.iswinning(tl2[0:i]+tl2[i+1:j]
                                    +tl2[j+1:k]+tl2[k+1:m]+tl2[m+1:],eye=False)
                            if therest[0] == True:
                                return (True,therest[1],
                                        therest[2]+[[tl2[i],tl2[j],tl2[k],tl2[m]]])
        return (False,None,None)
        
    def move_lookup(x):
        mapping = ["nothing", "draw","take in","pong with joker",
                   "pong","gong","win"]
        if type(x) == int:
            return mapping[x%len(mapping)]
        for (i,item) in enumerate(mapping):
            if item == x:
                return i
        return mapping
    
      
        
class Hand():
    def __init__(self, **tiledic):
        self.hidden = []
        self.shown = []
        self.bonus = []
        for key,ls in tiledic.items():
            if key == 'hidden':
                self.hidden = ls
            elif key == 'shown':
                self.shown = ls
            elif key == 'bonus':
                self.bonus = ls
                
    def draw(self,tile):
        if tile.bonus:
            self.bonus.append(tile)
            return False
        self.hidden.append(tile)           
        return True
    
    def discard(self, n):
        return self.hidden.pop(n)
    
    def arange(self):
        self.hidden = sorted(self.hidden,key=lambda x: getattr(x, 'id'))
        return
    
    def takein(self,foreigntile,*n):
        group = [foreigntile] + [self.hidden[i] for i in n]
        group = sorted(group, key = lambda x: getattr(x, 'id'))
        n = sorted(n, reverse = True)
        for i in n:
            self.hidden.pop(i)
        self.shown += group
        return
    
    def deepcopyTileList(self,tilelist):
        return [Tiles(t.family, t.number) for t in tilelist]
    
    def makecopy(self, anonymize = True):
        if anonymize:
            hidden = [None for _ in self.hidden]
        else:
            hidden = self.deepcopyTileList(self.hidden)
        shown = self.deepcopyTileList(self.shown)
        bonus = self.deepcopyTileList(self.bonus)
        return Hand(hidden=hidden,shown=shown,bonus=bonus)
            
        
    def console_show(self,hidden=False,shown=True,bonus=True):
        ls = [[t.shortname() for t in K] for K in [self.bonus,self.shown,\
               self.hidden]]
        S_disp = "|".join(ls[0] + ls[1])
        if hidden:
            S_hidden = "|".join(ls[2])
        else:
            S_hidden = "|".join(['X' for t in self.hidden])
        S_hidden = "|" + S_hidden + "|"
        lS = len(S_hidden)
        print('\n',S_disp,'\n','-'*lS,'\n',S_hidden)
    
class Game():
    # typically we play without joker, and with 4 players and characters tiles
    def __init__(self,characters = True, joker = False, 
                 bonus = True, dragons = True, winds = True, players = 4):
        self.players = players
        self.alltiles = []
        for q in range(4):
            for i in range(1,10):
                self.alltiles.append(Tiles('bamboo',i))
                self.alltiles.append(Tiles('dots',i))
                if characters:
                    self.alltiles.append(Tiles('characters',i))
                if i < 4:
                    if dragons:
                        self.alltiles.append(Tiles('dragons',i))
                if i < 5:        
                    if winds:
                        self.alltiles.append(Tiles('winds',i))

            if joker:
                self.alltiles.append(Tiles("joker",0))
            if bonus:
                self.alltiles.append(Tiles("flowers",q+1))
                self.alltiles.append(Tiles("seasons",q+1))
            
        random.shuffle(self.alltiles)
        
        #self.alltiles_name = [k.shortname() for k in self.alltiles]
        
        self.drawpointer = 0
        self.flowerpointer = len(self.alltiles)-1
        self.playerhands = [Hand() for _ in range(players)]
        self.discardpile = []
        
        
        self.gamelog = [("player","action","tile","combination")]
        self.statedescriptions = ['start','drawn','drawnfp','ate','pong','gong',
                                  'discard','out of cards','end']
        self.state = ("start",0) # state, currentplayer
        
        self.distribute_tiles()
        self.last_taken_in = (None,None)
        
        
        return 
       
    def statemapping(self, state):
        mapping = self.statedescriptions
        if type(state) == int:
            return mapping[state%len(mapping)]
        for i in range(len(mapping)):
            if mapping[i] == state:
                return i
        return "state mapping failed"
    
    def distribute_tiles(self):
        for _ in range(3):
            for i in range(self.players):   
                self.draw(i,4,False)
        for i in range(self.players):   
            self.draw(i,1,False)       
        self.draw(0,1,False) # player 0 gets 1 extra
            
        ntiles = [0]*self.players
        target = [14] + [13]*(self.players -1)
        while ntiles != target:
            for i in range(self.players):
                ntiles[i] = len(self.playerhands[i].hidden)
                diff = target[i] - ntiles[i]
                self.draw_end(i, diff,False)
        self.state = ("drawn",0)
        
        
        
        
    def previous_player(self):
        currentplayer = self.state[1]
        if currentplayer == 0:
            return self.players - 1
        return currentplayer - 1
    
    def next_player(self, n=1):
        currentplayer = self.state[1]
        return (currentplayer + n)%self.players
        
    
    def draw(self,player,n = 1,record=True):
        for _ in range(n):
            tile = self.alltiles[self.drawpointer]
            self.playerhands[player].draw(tile)
            self.drawpointer += 1
            if record:
                self.gamelog.append((player,"drawn",None,None))
        self.state = ("drawn",self.next_player())
        return
    
    def draw_end(self,player,n=1,record = True):
        for _ in range(n):
            tile = self.alltiles[self.flowerpointer]
            self.playerhands[player].draw(tile)
            self.flowerpointer -= 1
            if record:
                self.gamelog.append((player,"drawfp",None,None))
        return
        
    def discard(self, player,n):
        discardedtile = self.playerhands[player].discard(n)
        self.discardpile.append(discardedtile)
        return
        

    
    def can_eat(self, player):
        (tf,pos_ind,pos_group) = Rules.can_form_group(self.discardpile[-1],
                                    self.playerhands[player])
        if tf:
            return (tf,pos_ind,pos_group)
        return False
        
    def can_pong(self, player):
        (count,ind) = Rules.nsame(self.discardpile[-1],self.playerhands[player])
        if count > 1:
            return (True,ind[0:2])
        return False
    
    def can_gong(self,player):
        (count,ind) = Rules.nsame(self.discardpile[-1],self.playerhands[player])
        if count > 2:
            return (True,ind[0:3])
        return False
    
    def can_win(self,player):
        # iswinning(tilelist, eye=True): return (True/False, winning type, grouping)
        (tf,wt,g) = Rules.iswinning(self.playerhands[player].hidden)
        if tf:
            return tf
        (tf,wt,g) = Rules.iswinning(self.playerhands[player].hidden \
                    + [self.discardpile[-1]])
        return tf
    
    
    def takein(self, player,*n):
        if len(self.discardpile) < 1: return False
        foreigntile = self.discardpile[-1]
        hand = self.playerhands[player]
        if not Rules.can("take in",foreigntile,hand,*n): return False
        foreigntile = self.discardpile.pop()
        self.last_taken_in = (foreigntile,
                              [self.playerhands[player].hidden[i] for i in n])
        self.playerhands[player].takein(foreigntile,*n)
        self.state = ("ate",player)
        triplet = self.playerhands[player].shown[-3::]
        self.gamelog.append((player,"take in",foreigntile,
                                [str(t) for t in triplet]))
            
        return True
                
    def pong(self,player,*n):
        if len(self.discardpile) < 1: return False
        foreigntile = self.discardpile[-1]
        hand = self.playerhands[player]
        if not Rules.can("pong",foreigntile,hand,*n): return False
        tf_ind = self.can_pong(player)
        if tf_ind:

            self.last_taken_in = (foreigntile,
                    [self.playerhands[player].hidden[i] for i in n])
            hand.takein(foreigntile,*n)
            self.discardpile.pop()
            self.state = ("pong", player)
            self.gamelog.append((player,"pong",foreigntile,
                                [foreigntile]*3))
            return True
        return False            
            
            
    def gong(self,player,*n):
        if len(self.discardpile) < 1: return False
        foreigntile = self.discardpile[-1]
        hand = self.playerhands[player]
        if not Rules.can("gong",foreigntile,hand,*n): return False
        tf_ind = self.can_gong(player)
        if tf_ind:
            foreigntile = self.discardpile[-1]
            self.last_taken_in = (foreigntile,
                [self.playerhands[player].hidden[i] for i in n])
            hand = self.playerhands[player]
            hand.takein(foreigntile,*n)
            self.discardpile.pop()
            self.draw_end(player)
            self.state = ("gong", player)
            self.gamelog.append((player,"gong",foreigntile,
                            [foreigntile]*4))
            return True
        return False

        
    def playerdiscard(self,n):
        _,player = self.state
        if n < len(self.playerhands[player].hidden):
            self.discard(player,n)
            self.state = ("discard", player)
            self.gamelog.append((player,"discard",
                                 str(self.discardpile[-1]),None))

    def next_player_moves(self,*steptuples):
        # steptuples: (choice, *n)
        # eg. next_player_moves((1,),(3,3,4),(0,))        
        # choice reminder (ranked from least to most significant): 
        #   mapping = ["do nothing", "draw","take in","pong with joker",
        #           "pong","gong","win"]
        # *n: index for 0,1: nothing, 3,4 - indices
        
        # returns a list of [(player#,(choicenumber,*n)),((player#,(choicenumber,*n)))]
        # (at most nplyaer-1 items.)
        mapping = Rules.move_lookup("help")
        number_of_choices = len(mapping)
        action_to_player = [None]*number_of_choices
        action_to_steptuple = [None]*number_of_choices
        players = tuple([self.next_player(i) for i in range(1,self.players)])
        print("steptuples = ",steptuples)
        for (i,(choice,*n)) in enumerate(steptuples):
            if type(choice) != int:
                choice = Rules.move_lookup(choice)
            if action_to_player[choice] == None:
                action_to_player[choice] = i
                action_to_steptuple[choice] = steptuples[i]
        #print(action_to_player)
        #print(action_to_steptuple)
        rankedoptions = []
        for k in range(len(action_to_player)-1,-1,-1):
            i = action_to_player[k]
            if i != None:
                #print("person selected player: ",players[i],"\n steptuples",steptuples[i])
                rankedoptions.append((players[i],action_to_steptuple[k]))
        rankedoptions.append((players[0],("draw",0)))
        return rankedoptions
    

        
    
    def printstate(self,printoutstr = True):
        #self.statedescriptions = ['start','drawn','ate','pong','gong',
        #                          'discard','out of cards','end']
        state, player = self.state        
        if type(state) == int:
            state = self.statemapping(state)
        if state == "start":
            outstr = "Game Start"
        elif state == "drawn":
            outstr = "player " + str(player) + " drawn"
        elif state == "ate":
            outstr = "player " + str(player) + " took in " \
                + str(self.last_taken_in)
        elif state in ["pong","gong"]:
            outstr = "player " + str(player) + " " + state + " " \
                + str(self.last_taken_in)
        
        elif state == "discard":
            outstr ="player " + str(player) + " discarded " \
                + str(self.discardpile[-1]) 
        elif state == "out of cards":
            outstr = "game over: out of cards"
        elif state == "end":
            outstr ="game over: winner is player " +  str(player)
        else:
            outstr = "state " + str(state) + " not recognized"

        if printoutstr: print(outstr)
        return outstr

    def savelog(self):
        script_dir = os.path.dirname(__file__) 
        log_dir = os.path.join(script_dir,'log')
        if not os.path.exists('log'):
            os.makedirs('log')
        name = 'gamelog_'
        i = 1
        fullname = name + str(i) + '.csv'
        while fullname in os.listdir(log_dir):
            i += 1
            fullname = name + str(i) + '.csv'
        
        fullpath = os.path.join(log_dir,fullname)
        with open(fullpath,mode='w',newline='') as logfile:
            writer = csv.writer(logfile, delimiter=',')
            writer.writerows(self.gamelog)
            


class Player():
    def __init__(self, playernumber = 1):
        self.strategy = "basic bot"
        self.playernumber = playernumber
    
    
    def makedecision(self,gamestate, 
                     handlists, discardpile, ntilesleft, gamelog):
        # handlist = [previous hand, own hand, next hand, next next hand]
        
        # the few situations where decision is needed
        # 1. you drawn/ate/pong/gong a tile, now you have to pick one to discard
        # 2. you drawn a tile, now you need to decide if you won, or to discard
        # 3. others discarded a tile, decide to pong/gong/ate/win/do nothing
        
        # states = ['start','drawn','discard','out of cards','end']
        # gamestate = [states[?], player#]
        # RETURN (decision, *n)
 
        #   mapping = ["do nothing", "draw","take in","pong with joker",
        #           "pong","gong","win"]

        if gamestate[0] == "discard": # somebody discarded, do you pong, eat, gong, nothing?
            return self.action_take_simple(gamestate,handlists,discardpile,
                                      ntilesleft,gamelog)
            
        if gamestate[0] == "drawn": # you drawn
            winornot_decide = self.action_win_simple(gamestate,handlists,
                                            discardpile,ntilesleft,gamelog)
            if winornot_decide:
                return ('win',None)
            i = self.discard_simple(gamestate,handlists,discardpile,
                                    ntilesleft,gamelog)
            return (None, i)

        if gamestate[0] in ["ate","pong","gong"]: #what do you discard?
            i = self.discard_simple(gamestate,handlists,discardpile,
                                    ntilesleft,gamelog)
            return (None, i)

        return 0
    
    def discard_simple(self,gamestate,handlists,discardpile,ntilesleft,gamelog):
        minn = 14
        mini = 0
        for (i,t) in enumerate(handlists[1].hidden):
            n = Rules.relatable_to_hand(t,handlists[1]) 
            if n < minn:
                (minn,mini) = (n,i)
        return mini
    
    def action_win_simple(self,gamestate,handlists,discardpile,ntilesleft,gamelog):
        if len(discardpile) < 1:return False
        group = handlists[1].hidden + [discardpile[-1]]
        winningornot = Rules.iswinning(group)[0]
        return winningornot
    
    def action_take_simple(self,gamestate,handlists,discardpile,ntilesleft,gamelog):
        decision = random.choice(["gong","pong","eat","nothing","draw"])
        print("-----decision-------",decision)
        indices = [i for i in range(len(handlists[1].hidden))]
        four = []
        for k in range(4):
            l = len(indices)
            randi = random.randint(0,l-1)
            four.append(indices.pop(randi))
        
        if decision in ["draw","nothing"]:
            return ("nothing",[])
        if decision == "eat":
            return ("take in",*four[:3])
        if decision == "pong":
            return ("pong",*four[:3])
        if decision == "gong":
            return ("gong",*four[:4])
        if decision == "win":
            return ("win",[])
        return ("nothing",[])
    
    
    
class HumanPlayer(Player):
    def __init__(self,playernumber = 1):
        super().__init__(playernumber)
        self.strategy = "human!"
        
    def makedecision(self,gamestate,
                     handlists,discardpile, ntileleft, gamelog):
        # states = ['start','drawn','discard','out of cards','end']
        # gamestate = [states[?], player#]
        # RETURN (decision, *n)
    
        print("------------------------------------")
        print("Player ",self.playernumber)
        print("------------------------------------")
        
        handlists[1].console_show(hidden=True)
        
        #   mapping = ["do nothing", "draw","take in","pong with joker",
        #           "pong","gong","win"]
        lastplayer = gamestate[1]
        lastdiscard = None
        if discardpile:
            lastdiscard = discardpile[-1]
        if gamestate[0] == "discard": # somebody discarded, do you pong, eat, gong, nothing?
            outstr = "player "+str(lastplayer) +" discarded Tile " \
                        + str(lastdiscard) \
                        + self.makeactionstring((0,"nothing"),(1,"draw"),
                                                (2,"eat"),(3,"pong"),
                                                (4,"gong"),(5,"win")) # WINNING NOT settled yet!     
            decision = int(self.getuserresponse(outstr, [0,1,2,3,4,5]))
            
            if decision in [0,1]:
                return ("nothing",[])
            if decision == 2:
                indexlist = self.askwhichtiles(2,handlists[1])
                return ("take in",*indexlist)
            if decision == 3:
                indexlist = self.askwhichtiles(2,handlists[1])
                return ("pong",*indexlist)
            if decision == 4:
                indexlist = self.askwhichtiles(3,handlists[1])
                return ("gong",*indexlist)
            if decision == 5:
                return ("win",[])
            
        if gamestate[0] == "drawn": # you drawn
            outstr = "0 - discard, 1 - claim victory \n"
            decision = int(self.getuserresponse(outstr,[0,1]))
            if decision == 1: # claim victory
                return ('win',None)
            i_discard = self.askwhichtiles(1,handlists[1])[0]
            print("i_discard = ",i_discard)
            return (None,i_discard)
            
        if gamestate[0] in ["ate","pong","gong"]: #/ate/pong/gong or win?, what do you discard?
            i_discard = self.askwhichtiles(1,handlists[1])[0]
            return (None,i_discard)
            
    def askwhichtiles(self,n,hand):
        handstr1 = " "
        handstr2 = "|"
        for (i,t) in enumerate(hand.hidden):
            tstr = str(t)
            l = len(tstr) 
            handstr2 += tstr + "|"
            numberstr = " " + str(i) + " "*(l-len(str(i)))
            handstr1 += numberstr
        print("Select ",str(n), " tiles")
        print(handstr1,"\n", handstr2, "\n")
        ls = []
        while True:
            val = input()
            try:
                val = int(val)
                if val < 0 or val >= len(hand.hidden):
                    print("out of range")
                else:
                    if val not in ls:
                        ls.append(val)
            except ValueError:
                print("integer please")
            
            if len(ls) == n:
                break
        return ls
            
            
    
            
            
            
    def makeactionstring(self,*intwordtuple):
        outstr = "\n What is your action? \n"
        for (i,word) in intwordtuple:
            outstr += str(i)+" - " + word + "\n"
        return outstr
        
    def getuserresponse(self,outstr,expected):
        ex = [str(i) for i in expected]
        val = ""
        while True:
            val = input(outstr + '\n')
            if expected:
                if val in ex:
                    return val
                print('\n Value not recognized.' + outstr)
            else:
                return val
        
        
        
        
     
class GameManager(Game):
    def __init__(self, playerinstancelist = [HumanPlayer(1),Player(2),
                        Player(3),Player(4)],autoarrange = True,**options):
        self.playerlist = playerinstancelist
        super().__init__(players = len(self.playerlist,**options))
        
        self.autoarrange = autoarrange

    def startgame(self):
        
        #makedecision(self,gamestate,
        #             handlists,discardpile, ntileleft, gamelog):
        # states = ['start','drawn','discard','out of cards','end']
        # gamestate = [states[?], player#]
        # RETURN (decision, n)

        while True:
            print("game.state = ", game.state)
            if self.autoarrange:
                for hand in self.playerhands:
                    hand.arange()
                    
            
            if self.state[0] in ["drawn","pong","ate","gong"]: 
                # some player drawn. Ask for decision (which tile to discard)
                playertoact = self.playerlist[self.state[1]]
  
                info_forplayer = self.pass_info_to_player(self.state[1])
                self.printstate()
                (decision,*n) = playertoact.makedecision(self.state,*info_forplayer)
                
                print("decision: ",decision, " \n n: ", n)
                
                i = n[0]
                self.playerdiscard(i)
                #self.gamelog.append((self.state[1],"discard",
                #                    str(self.discardpile[-1]),
                #                    None))
                
            elif self.state[0] == "discard":
                # some player discard a tile. Ask everyone for a decision
                every_player_choose = []
                for i in range(1,self.players):
                    p = self.next_player(i)
                    playertoact = self.playerlist[p]
                    info_forplayer = self.pass_info_to_player(p)
                    (decision,*n) = playertoact.makedecision(self.state,*info_forplayer)
                    print("decision: ",decision, " \n n: ", n)
                    every_player_choose.append([decision,*n])
                print(every_player_choose)
                rankedoptions = self.next_player_moves(*every_player_choose)
                print(rankedoptions)
                self.dotherankedmoves(rankedoptions)
                
                    

            elif self.state[0] == "out of cards":
                # out of cards
                break
            
            elif self.state[0] == "end":
                # end game
                break
            
            else:
                print("state ",self.state[0], " not recognized")
                break
            
            
        print("++++++++++++ Hope you enjoyed the game ++++++++++++++++++")
                
        
    def dotherankedmoves(self,rankedoptions):
        for playernumber,(choice,*n) in rankedoptions:
            if self.dothemove(playernumber,choice,*n)==True:
                self.printstate()
                return
       
                
    def dothemove(self,player,choice,*n):
        move = choice
        if type(choice) == int:
            move = Rules.move_lookup(choice)
            
        if move in ["nothing","draw"]:
            self.draw(self.next_player())
            return True
            
        elif move == "take in":
            if self.takein(player,*n):return True
            #self.notifystate(['take in ',player])
            
            
        elif move == "pong":
            if self.pong(player,*n):return True
            #self.notifystate(['pong',player])
            
        elif move == "gong":
            if self.gong(player,*n): return True
            #self.notifystate(['gong',player])
            
        elif move == "win":
            if self.can_win(player):
                self.gamelog.append((player,"win",None,None))
                self.state = (4,player)
                return True

        
        
    def notifystate(self,special = None): # special = ['pong',3]
        gamestate = self.state
        # states = ['start','drawn','discard','out of cards','end']
        # gamestate = [states[?], player#]
        if special:
            outstr = "Player " + str(special[1])+ " " + special[0] + "\n"
            print(outstr)
            return
        if gamestate[0] == 0:
            outstr = "Game start!\n"
        elif gamestate[0] == 1:
            outstr = "Player "+str(gamestate[1])+ " drawn "
        elif gamestate[0] == 2:
            outstr = "Player " + str(gamestate[2])+" discarded Tile " \
                + str(self.discardpile[-1])
        elif gamestate[0] == 3:
            outstr = "game over: out of cards! no winner!\n"
        else:
            outstr = "game over, the winner is player "+str(gamestate[1])+ "!"
        print(outstr)
        return
        
    
    def pass_info_to_player(self,n):
        # return the state of affairs: 
        # ([previous hand, own hand, next hand, next next hand],
        #        discardedpile, ntilesleft,gamelog)
        ownhand = self.playerhands[n].makecopy(anonymize = False)
        previous = self.playerhands[(n-1)%(self.players)].makecopy()
        nexthand = self.playerhands[(n+1)%(self.players)].makecopy()
        next2hand = self.playerhands[(n+2)%(self.players)].makecopy()
        ntilesleft = self.flowerpointer - self.drawpointer + 1
        discardpile = [Tiles(t.family, t.number) for t in self.discardpile]
        gamelog = [item for item in self.gamelog]
        return ([previous,ownhand,nexthand,next2hand],
                discardpile,ntilesleft,gamelog)

    
playerinstancelist = [HumanPlayer(0),HumanPlayer(1),
                      HumanPlayer(2),HumanPlayer(3)]
playerinstancelist = [Player(0),Player(1),
                      HumanPlayer(2),Player(3)]    
game = GameManager(playerinstancelist=playerinstancelist)

for i in range(4):
    print("player ",i)
    game.playerhands[i].console_show(hidden=True)


game.startgame()
    
    
#bot = Player(1)
#human = HumanPlayer(1)

#pass_info_to_player(self,n):
        # return the state of affairs: 
        # ([previous hand, own hand, next hand, next next hand],
        #        discardedpile, ntilesleft,gamelog)
#(handlists,_,_,_) = game.pass_info_to_player(1)
#makedecision(self,gamestate,handlists,discardpile, ntileleft, gamelog)
#human.makedecision((2,1),handlists,[Tiles('bamboo',3)],1,1)



     
        
"""       
t0 = Tiles('bamboo',1)      
t1 = Tiles('bamboo',1)
t2 = Tiles('characters',2)    
t3 = Tiles('winds',1)
t4 = Tiles('flowers',3)
t5 = Tiles('bamboo',6)
t6 = Tiles('bamboo',5)
t7 = Tiles('bamboo',4)
t8 = Tiles('bamboo',1)
hand = Hand(hidden=[t1,t2,t2,t3,t1],shown = [t2],bonus=[t4])  
hand.console_show(hidden=True)
hand.arange()
hand.console_show(hidden=True)
game = Game()

print(len(game.alltiles))

game.playerhands[0].console_show(hidden=True)
game.playerhands[1].console_show(hidden=True)
game.playerhands[2].console_show(hidden=True)
game.playerhands[3].console_show(hidden=True)

print("draw pointer ", game.drawpointer, "| flowerdraw pointer", game.flowerpointer)



print("\n","TEST RULES", "\n")
assert(Rules.ispair(t0,t1)==True)
assert(Rules.ispair(t0,t7)==False)
assert(Rules.ispair(t0,t7,t0)==False)
print("pair test pass")
assert(Rules.istriplet_distinct(t5,t6,t7)==True)
assert(Rules.istriplet_distinct(t6,t5,t7)==True)
assert(Rules.istriplet_distinct(t6,t7,t5)==True)
assert(Rules.istriplet_distinct(t6,t7,t6)==False)
print("triplet nonidentical test pass")

assert(Rules.istriplet_identical(t6,t5,t7)==False)
assert(Rules.istriplet_identical(t6,t7,t5)==False)
assert(Rules.istriplet_identical(t1,t0,t8)==True)
print("triplet identical test pass")

assert(Rules.istriplet(t6,t7,t5)==True)
assert(Rules.istriplet(t6,t7,t6)==False)
assert(Rules.istriplet(t1,t0,t8)==True)
print("generic triplet test pass")


a = [Tiles('characters',3),Tiles('characters',4),Tiles('characters',5)]
b = [Tiles('winds',3),Tiles('winds',3),Tiles('winds',3)]
c = [Tiles('bamboo',8),Tiles('bamboo',8),Tiles('bamboo',8)]
d = [Tiles('dragons',3),Tiles('dragons',3),Tiles('dragons',3)]
e = [Tiles('dragons',3),Tiles('dragons',3),Tiles('dragons',3),Tiles('dragons',3)]
f = [Tiles('dots',5),Tiles('dots',5)]

ls = a+b+c+d+f
ls2 = a+b+c+e+f
thirteen = [Tiles('winds',1),Tiles('winds',2),
                      Tiles('winds',3),Tiles('winds',4),Tiles('dragons',1),
                      Tiles('dragons',2),Tiles('dragons',3), Tiles('bamboo',1),
                      Tiles('bamboo',9), Tiles('characters',1), 
                      Tiles('characters',9),Tiles('dots',1), Tiles('dots',9)]
random.shuffle(ls)
random.shuffle(ls2)
print(ls)

p1 = Rules.iswinning(ls)
p2 = Rules.iswinning(ls2)
p3 = Rules.iswinning(thirteen)
assert(p1[0] == True)
assert(p2[0] == True)
assert(p3[0]==True)
print(p1[2])
print(p2[2])
print(p3[2])
print("winning test pass")


"""

