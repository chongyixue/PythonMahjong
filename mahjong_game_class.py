# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 18:29:35 2021

@author: chong
"""

from mahjong_components import Tiles, Hand
from mahjong_rules import Rules
import csv,os,random
from mahjong_players import Player, HumanPlayer

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
    
    def win(self,player):
        if self.can_win(player):
            self.gamelog.append((player,"win",None,None))
            self.state = ("win",player)
            return True
        

        
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
        elif state in ["end","win"]:
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
            print("game.state = ", self.state)
            if self.autoarrange:
                for hand in self.playerhands:
                    hand.arange()
                    
            
            if self.state[0] in ["drawn","pong","ate","gong"]: 
                # some player drawn. Ask for decision (which tile to discard)
                playertoact = self.playerlist[self.state[1]]
                info_forplayer = self.pass_info_to_player(self.state[1])
                
                # protection against rogue answers
                canwin = True
                chances = 3
                for _ in range(chances):
                    (decision,*n) = playertoact.makedecision(self.state,*info_forplayer)
                    print("decision ",decision, "  n=",n)
                    if decision == "win" and canwin:
                        canwin = self.win(self.state[1])
                        print(canwin)
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
            
            elif self.state[0] in ["win", "end"]:
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
            if self.win(player): 
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
        
    def cheat(self,option='almost winning',player=1):
        if option == 'almost winning':
            self.playerhands[player].shown = []
            self.playerhands[player].hidden = [Tiles('bamboo',4),
                            Tiles('bamboo',5),Tiles('bamboo',6),
                            Tiles('dragons',1),Tiles('dragons',1),
                            Tiles('dragons',1),Tiles('winds',1),
                            Tiles('winds',1),Tiles('winds',1),
                            Tiles('dots',1),Tiles('dots',1),Tiles('dragons',2),
                            Tiles('dragons',2)]
            self.discardpile.append(Tiles('dragons',2))
            self.state = ('discard' , (player+1)%self.players)
            self.startgame()
            
        elif option == "win not discard":
            self.playerhands[player].shown = []
            self.playerhands[player].hidden = [Tiles('bamboo',4),
                            Tiles('bamboo',5),Tiles('bamboo',6),
                            Tiles('dragons',1),Tiles('dragons',1),
                            Tiles('dragons',1),Tiles('winds',1),
                            Tiles('winds',1),Tiles('winds',1),
                            Tiles('dots',1),Tiles('dots',1),Tiles('dragons',2),
                            Tiles('dragons',2),Tiles('dragons',2)]
            self.discardpile.append(Tiles('dragons',3))
            self.state = ('drawn' , player)
            self.startgame()
    
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


