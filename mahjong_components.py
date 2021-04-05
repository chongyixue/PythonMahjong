# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 18:25:20 2021

@author: chong
"""



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
        if other:
            return self.id == other.id
        return False
    def __sub__(self,other):
        if not self.suits or not other.suits:
            return (1 - 1*(self == other))*100
        if self.family != other.family:
            return 100
        return self.id - other.id
    # None is "smallest"
    def __lt__(self,other):
        if other:
            return self.id < other.id
        return True
    def __gt__(self,other):
        if other:
            return self.id > other.id
        return False        

    
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
    