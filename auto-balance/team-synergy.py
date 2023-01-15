import pandas as pd
import json
from statistics import mean
import numpy as np
from pprint import pprint 
from xgboost import XGBRegressor
import copy 

''' LOADING THE DATA '''
data_source_file = "./data-frame-friendly.json" #this should be changed 
f = open (data_source_file, "r")
data = json.load(f)
df1 = pd.DataFrame.from_dict(data, orient='index')
df1=df1.reset_index()

full_dict_storage = [] 
#0 player did not play 
#1 player is loser 
#2 player is winner

''' CLEANING DATA LOADED '''
for index,row in df1.iterrows(): 
    
    player_names ={
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
    "yang_acs":0,
    "score_diff":0}
    
    min_team_size = min(len(row["team_red"]),len(row["team_blue"]))
#     print(min_team_size)
    if row["score_red"] > row["score_blue"]: # this means team a won 

#         print(row["team_red"][0]["player_name"])
        for index_2 in range(0,min_team_size,1): # go from 0 to five #HUGE BUG HERE 
        
            row_data = row["team_red"][index_2]
            #doing team a player assignment
            name = row["team_red"][index_2]["player_name"]
            player_names[name] = player_names.get(name, 0) + 2
            
            # doing the other team assignment 
            name = row["team_blue"][index_2]["player_name"]
            player_names[name] = player_names.get(name, 0) + 1
            
            #adding acs data 
            name = row["team_red"][index_2]["player_name"]
            new_dict_label = str(name)+"_acs"
            player_names[new_dict_label] = player_names.get(new_dict_label, 0) + row["team_red"][index_2]["average_combat_score"]
            
            name = row["team_blue"][index_2]["player_name"]
            new_dict_label = str(name)+"_acs"
            player_names[new_dict_label] = player_names.get(new_dict_label, 0) + row["team_red"][index_2]["average_combat_score"]


    elif row["score_red"] < row["score_blue"]: # this means team b won 
        for index_2 in range(0,min_team_size,1): # go from 0 to five
            name = row["team_red"][index_2]["player_name"]
            player_names[name] = player_names.get(name, 0) + 1
            
            # doing the other team assignment 
            name = row["team_blue"][index_2]["player_name"]
            player_names[name] = player_names.get(name, 0) + 2
            
            #adding acs data 
            name = row["team_red"][index_2]["player_name"]
            new_dict_label = str(name)+"_acs"
            player_names[new_dict_label] = player_names.get(new_dict_label, 0) + row["team_red"][index_2]["average_combat_score"]
            
            name = row["team_blue"][index_2]["player_name"]
            new_dict_label = str(name)+"_acs"
            player_names[new_dict_label] = player_names.get(new_dict_label, 0) + row["team_red"][index_2]["average_combat_score"]

    player_names['score_diff'] = abs(row["score_red"] - row["score_blue"]) # i think i take abs value
#     player_names['score_diff'] = row["score_red"] - row["score_blue"]
    # print(player_names) # UNCOMMENT THIS TO SHOW RESULTS 
    
    full_dict_storage.append(player_names)
#     break

df_generated = pd.DataFrame.from_dict(full_dict_storage)
df_generated = df_generated.replace(np.nan,0) 

''' PREPARE FOR MODEL TRAINING'''

# select the x_train columns 
x_train= df_generated[["andy",
    "brandon",
    "brian",
    "cade",
    "darwin",
    "josh",
    "lindsey",
    "sequential",
    "sophie",
    "steve",
    "steven",
    "sun",
    "susi",
    "susu",
    "tang",
    "yang",
    "andy_acs",
    "brandon_acs",
    "brian_acs",
    "cade_acs",
    "darwin_acs",
    "josh_acs",
    "lindsey_acs",
    "sequential_acs",
    "sophie_acs",
    "steve_acs",
    "steven_acs",
    "sun_acs",
    "susi_acs",
    "susu_acs",
    "tang_acs",
    "yang_acs"]]

# x_train = df_generated.iloc[:,:16]
x_train = x_train.to_numpy()
# move column position  https://www.geeksforgeeks.org/how-to-move-a-column-to-first-position-in-pandas-dataframe/
y_train = df_generated[["score_diff"]]
y_train = y_train.to_numpy()

xgb_model = XGBRegressor()
# model = XGBRegressor(n_estimators=1000, max_depth=7, eta=0.1, subsample=0.7, colsample_bytree=0.8)# try linear parameter and other stuff 
# paramenters can be better tuned 
# learning rate will affect the results!!!
xgb_model = XGBRegressor(nthread=-1, seed=500, eval_metric="rmse", n_estimators=300,learning_rate=1)
xgb_model.fit(x_train,y_train)


''' RUN ALL COMBINATIONS'''

import itertools
# this is where you input the player names and map 
players = ["andy","darwin","steve","steven","sophie","brandon","lindsey","josh","susu","cade"] # 10 players
map_name = "Icebox"
print('num of players',len(players)) # players should be 10, only works with 10 players

all_combinations = []
for comb in itertools.combinations(players, 5):
    both_combs = {} 
    
    comb = list(comb) # first combination
    both_combs[1] = comb
    
    # run every possible combination of 10 choose 5 
    other_comb = list(set(players)-set(comb))# other combination 
    both_combs[2] = other_comb
    
#     print(other_comb)
    all_combinations.append(both_combs) 
# all_combinations


 #https://www.geeksforgeeks.org/read-json-file-using-python/
# data_source_file = "./data copy.json"
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


### calculate player acs 
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

'''NOW WE PREDICT FOR EACH PLAYER'''
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

'''Predict score difference of every combination of players in 2 teams (10 choose 5)'''
        
all_combs_storage =[]

# this step is creating each x_train from each combintation 
for i in all_combinations:
    # this is the first 252 combinations (where we think 2 will be the winning team as trained in the model)

    player_names = copy.deepcopy(player_x_predict) #need this to copy the acs per person

    for name in i[1]: # person who is 2 matters more 
        player_names[name] = player_names.get(name, 0) + 1 #assign to team 1

    for name in i[2]: 
        player_names[name] = player_names.get(name, 0) + 2 #assign to team 2
    
    y_data= list(player_names.values())
    y_predict = xgb_model.predict([y_data])
    
#     print(player_names.keys(),y_predict)
    y_predict = float(y_predict)
    answer = {} 
    answer[y_predict]= player_names
    all_combs_storage.append(answer)
    
    #-----------------------------------------------------------------------------
    #now we have to do the next 252 combinations and flip 1 and 2s (2s will be the winning team)
    player_names = copy.deepcopy(player_x_predict) #need this to copy the acs per person

    for name in i[1]: # person who is 2 matters more 
        player_names[name] = player_names.get(name, 0) + 1 #assign to team 1

    for name in i[2]: 
        player_names[name] = player_names.get(name, 0) + 2 #assign to team 2
        
    y_data= list(player_names.values())
    y_predict = xgb_model.predict([y_data])
    
#     print(player_names.keys(),y_predict)
    y_predict = float(y_predict)
    answer = {} 
    answer[y_predict]= player_names
    all_combs_storage.append(answer)
    
''' Find the smallest predicted score differences in all combinations '''
final_answer = [] 
smallest_value = 99
for i in all_combs_storage:
    for k, v in i.items():
        if float(k) <smallest_value: 
            smallest_value = float(k)
            final_answer = i  
            
### Find players who were assigned to team 1 and team 2 

team_1 = [] 
team_2 = [] 
for key,values in final_answer.items(): 
    counter = 0 # stop after 17
    for keys2,values2 in values.items(): 
#         print(keys2,values2)
        
        if counter <= 17: #there are 17 players
            if values2 == 1: 
                team_1.append(keys2)
            elif values2 == 2: 
                team_2.append(keys2)

            counter = counter + 1 
            
print('Predicted score difference:',smallest_value)            
print(team_1)
print(team_2)