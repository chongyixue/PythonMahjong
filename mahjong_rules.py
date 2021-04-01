# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 18:32:53 2021

@author: chong
"""

from mahjong_components import Tiles

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
    
      
        