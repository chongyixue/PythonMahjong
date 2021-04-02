# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 09:20:06 2021

@author: chong
"""

from mahjong_components import *
from mahjong_players import *
from mahjong_rules import *
from mahjong_game_class import *

      

    
playerinstancelist = [HumanPlayer(0),HumanPlayer(1),
                      HumanPlayer(2),HumanPlayer(3)]
playerinstancelist = [Player(0),HumanPlayer(1),
                      Player(2),Player(3)]    
game = GameManager(playerinstancelist=playerinstancelist)
game.cheat('win not discard')



#game.startgame()
    


     

