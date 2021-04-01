# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 09:20:06 2021

@author: chong
"""

from mahjong_components import *
from mahjong_players import *
from mahjong_rules import *
from mahjong_game_class import *

      

    

    


     
        
    
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




