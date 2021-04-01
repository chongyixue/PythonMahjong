# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 18:37:22 2021

@author: chong
"""


from mahjong_rules import Rules
import random

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
        
        
        