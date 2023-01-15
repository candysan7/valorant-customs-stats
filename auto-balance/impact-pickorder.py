''' PICK ORDER BY RANK '''
import pandas as pd
import json
from statistics import mean
import numpy as np
from pprint import pprint 
from xgboost import XGBRegressor
import copy 

# this is where you input the player names and map 
players = ["andy","darwin","steve","steven","sophie","brandon","lindsey","josh","susu","cade"] # 10 players
map_name = "Icebox"
print('num of players entered',len(players))

rank_storage = {
    "andy":2,
    "brandon":15,
    "brian":14,
    "cade":5,
    "darwin":7,
    "josh":9,
    "lindsey":6,
    "sequential":1,
    "sophie":11,
    "steve":10,
    "steven":3,
    "sun":8,
    "susi":12,
    "susu":13,
    "tang":4,
    "yang":16,
}

rank_storage=dict(sorted(rank_storage.items(), key=lambda x: x[1])) # sorting 

# find players who arent involved 
players_not_involved = []
for names,values in rank_storage.items(): 
    if names not in players:
        players_not_involved.append(names)

# print(players_not_involved)

# now remove the people not involved
for remove_name in players_not_involved: 
    rank_storage.pop(remove_name)

'''ADD NEW PLAYER HERE '''
# # ### add new player here 
# final_answer_sliced['brandon_brother'] = 3.5


# #print(final_answer_sliced)
''' SORTING TEAMS BY ACS '''

# # https://arxiv.org/pdf/2012.10171.pdf#:~:text=Drafting%20alternates%20between%20two%20teams,two%20heroes%2C%20and%20so%20on.
# #"1-2-2-1-1-2-2-1-1-2"
team_1_players = []
team_2_players = []
# ABBAABBABA
team_1_order = [0,3,4,7,8] 
team_2_order = [1,2,5,6,9] 

# find optimal pick order.... 
counter = 0 
for keys,values in rank_storage.items():
    
    if counter <=9: 
        index = index = list(rank_storage).index(keys) #keys = "andy" # get the index per key 
        if index in team_1_order: 
            team_1_players.append(keys)
#             print(keys)
        else: 
            team_2_players.append(keys)
#             print('2',keys)
    #     print(keys,values)
    counter += 1 
    
print(team_1_players,team_2_players)



