''' PICK ORDER BY ACS '''
import pandas as pd
import json
from statistics import mean
import numpy as np
from pprint import pprint 
from xgboost import XGBRegressor
import copy 
import itertools


def calc_player_acs(player_name,map_name): # we are taking the top
#     player_name = "brian"
    # def calc_player_average

    recent3_maps = new_df.loc[(new_df['player_name']==player_name)&(new_df['map']==map_name)]['average_combat_score'][-5:].tolist()
    recent3_games = new_df.loc[(new_df['player_name']==player_name)]['average_combat_score'][-5:].tolist()

    all_scores = set(recent3_maps + recent3_games) # appends here does not add

    # we take the mean of here
    average_acs = sum(all_scores) / len(all_scores)
    # print(len(all_scores))
    
    return average_acs


data_source_file = "./data-frame-friendly.json"

f = open (data_source_file, "r")
data = json.load(f)
df1 = pd.DataFrame.from_dict(data, orient='index')
df1=df1.reset_index()

### we flatten the df here 
row_storage = []

for main_index,main_row in df1.iterrows(): 
#     print(main_index)
    meta_data = df1[['time','url','map','score_red','score_blue']].iloc[main_index]

    teams = ["team_red","team_blue"]

    for team_number in teams:
        df2 = pd.json_normalize(df1[team_number].iloc[main_index]) #take the first row 


        for index,row in df2.iterrows():
            new_row = pd.concat([meta_data, row])
            row_storage.append(new_row)

new_df = pd.DataFrame(row_storage)

# this is where you input the player names and map 
players = ["andy","darwin","yang","steven","susu","steve","lindsey","josh","cade","sophie"] # 10 players
map_name = "Icebox"
print('num of players entered',len(players))

player_x_predict = {
    "andy":0,
    "brandon":0,
    "brian":0,
    "cade":0,
    "darwin":0,
    "josh":0,
    "lindsey":0,
    "sequential":0,
    "sophie":0,
    "steve":0,
    "steven":0,
    "sun":0,
    "susi":0,
    "susu":0,
    "tang":0,
    "yang":0,
    "andy_acs":0,
    "brandon_acs":0,
    "brian_acs":0,
    "cade_acs":0,
    "darwin_acs":0,
    "josh_acs":0,
    "lindsey_acs":0,
    "sequential_acs":0,
    "sophie_acs":0,
    "steve_acs":0,
    "steven_acs":0,
    "sun_acs":0,
    "susi_acs":0,
    "susu_acs":0,
    "tang_acs":0,
    "yang_acs":0}

for p_name in players: 
    acs_average = calc_player_acs(p_name,map_name)
    key_name = p_name + "_acs" # we are "predicting" the player's acs by taking their average 
    player_x_predict[key_name] = player_x_predict.get(key_name, 0) + acs_average


'''ADD NEW PLAYER HERE '''
# # ### add new player here 
# final_answer_sliced['brandon_brother'] = 150

# need to sort from greatest to least
final_answer_sliced=dict(sorted(player_x_predict.items(), key=lambda x: -x[1]))


#print(final_answer_sliced)
''' SORTING TEAMS BY ACS '''

# https://arxiv.org/pdf/2012.10171.pdf#:~:text=Drafting%20alternates%20between%20two%20teams,two%20heroes%2C%20and%20so%20on.
#"1-2-2-1-1-2-2-1-1-2"
team_1_players = []
team_2_players = []
# ABBAABBABA
team_1_order = [0,3,4,7,8] 
team_2_order = [1,2,5,6,9] 

# find optimal pick order.... 
counter = 0 
for keys,values in final_answer_sliced.items():
    
    if counter <=9: 
        index = index = list(final_answer_sliced).index(keys) #keys = "andy" # get the index per key 
        if index in team_1_order: 
            team_1_players.append(keys)
#             print(keys)
        else: 
            team_2_players.append(keys)
#             print('2',keys)
    #     print(keys,values)
    counter += 1 
    
print(sorted(team_1_players))
print(sorted(team_2_players))



