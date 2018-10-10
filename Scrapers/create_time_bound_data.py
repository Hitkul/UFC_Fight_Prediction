import json
import datetime
import time
from os import listdir
from os.path import isfile, join



def get_fighter_profile_template():
    with open('data/fighter_profile_template.json') as data_file:
        return json.load(data_file)

def get_all_results():
    with open('data/results_record.json') as data_file:    
        return json.load(data_file)

def get_name_of_all_fight_json():
    return [f for f in listdir("data/fight_json/") if isfile(join("data/fight_json/", f))]

def get_fighters_name_from_fight_json(data):
    try:
        return (data["FMLiveFeed"]["Fighters"]["Blue"]["Name"],data["FMLiveFeed"]["Fighters"]["Red"]["Name"])
    except KeyError: 
        fighter_details_block = data["FMLiveFeed"]["Fight"]["Fighters"]
        if fighter_details_block[0]["Color"] == "Blue":
            return (fighter_details_block[0]["Name"],fighter_details_block[1]["Name"])
        else:
            return (fighter_details_block[1]["Name"],fighter_details_block[0]["Name"])

def get_fighters_id_from_fight_json(data):
    try:
        return (data["FMLiveFeed"]["Fighters"]["Blue"]["FighterID"],data["FMLiveFeed"]["Fighters"]["Red"]["FighterID"])
    except KeyError: 
        fighter_details_block = data["FMLiveFeed"]["Fight"]["Fighters"]
        if fighter_details_block[0]["Color"] == "Blue":
            return (fighter_details_block[0]["Name"],fighter_details_block[1]["FighterID"])
        else:
            return (fighter_details_block[1]["Name"],fighter_details_block[0]["FighterID"])

def add_time_stamps(time1,time2):
    if time1 == "":
        time1 = "00:00:00"
    if time2 == "":
        time2="00:00:00"
    if time1.count(':') == 1:
        time1 = "00:"+time1
    if time2.count(':') == 1:
        time2 = "00:"+time2
    if time1.count(':') != 0:
        time1 =  datetime.datetime.strptime(time1, '%H:%M:%S')
        time1 = str(datetime.timedelta(hours=time1.hour,minutes=time1.minute,seconds=time1.second).total_seconds())
    if time2.count(':') != 0:
        time2 =  datetime.datetime.strptime(time2, '%H:%M:%S')
        time2 = str(datetime.timedelta(hours=time2.hour,minutes=time2.minute,seconds=time2.second).total_seconds())
    return str(float(time1)+float(time2))

def get_formated_int_value(value):
    if value == "":
        return 0
    elif value[-1] == '*':
        return int(value[:-1])
    else:
        return int(value)

def update_profile(data,id,i,winner_id):
    global fighters_profiles
    round_data_fight = data["FMLiveFeed"]["RoundStats"]
    round_data_fighter = fighters_profiles[id]["Fighter_stats"]
    # print winner_id
    if winner_id == "00000":
        fighters_profiles[id]["Record"].append(4)
    elif winner_id == "11111":
        fighters_profiles[id]["Record"].append(3)
    elif winner_id == id:
        fighters_profiles[id]["Record"].append(1)
    else:
        fighters_profiles[id]["Record"].append(0)
    for key in list(round_data_fight.keys()):
        if i == 0:
            for style in list(round_data_fight[key]["Blue"].keys()):
                if style == "Grappling" or style == "Strikes":
                    for move in list(round_data_fight[key]["Blue"][style].keys()):
                        for value in list(round_data_fight[key]["Blue"][style][move].keys()):
                            value_in_fight_data = round_data_fight[key]["Blue"][style][move][value]
                            value_in_fight_data = get_formated_int_value(value_in_fight_data)
                            value_in_fighter_profile = round_data_fighter[key][style][move][value]
                            value_in_fighter_profile = get_formated_int_value(value_in_fighter_profile)
                            value_in_fighter_profile+=value_in_fight_data
                            round_data_fighter[key][style][move][value] = str(value_in_fighter_profile)
                elif style == "TIP":
                    for move in list(round_data_fight[key]["Blue"][style].keys()):
                        value_in_fight_data = round_data_fight[key]["Blue"][style][move]
                        value_in_fighter_profile = round_data_fighter[key][style][move]
                        round_data_fighter[key][style][move] = add_time_stamps(value_in_fight_data,value_in_fighter_profile)
        else:
            for style in list(round_data_fight[key]["Red"].keys()):
                if style == "Grappling" or style == "Strikes":
                    for move in list(round_data_fight[key]["Red"][style].keys()):
                        for value in list(round_data_fight[key]["Red"][style][move].keys()):
                            value_in_fight_data = round_data_fight[key]["Red"][style][move][value]
                            value_in_fight_data = get_formated_int_value(value_in_fight_data)
                            value_in_fighter_profile = round_data_fighter[key][style][move][value]
                            value_in_fighter_profile = get_formated_int_value(value_in_fighter_profile)
                            value_in_fighter_profile+=value_in_fight_data
                            round_data_fighter[key][style][move][value] = str(value_in_fighter_profile)
                elif style == "TIP":
                    for move in list(round_data_fight[key]["Red"][style].keys()):
                        value_in_fight_data = round_data_fight[key]["Red"][style][move]
                        value_in_fighter_profile = round_data_fighter[key][style][move]
                        round_data_fighter[key][style][move] = add_time_stamps(value_in_fight_data,value_in_fighter_profile)

def master_loop(name_of_file):
    global result_of_fights
    global fighters_profiles
    global files_with_different_template
    winner_id = result_of_fights[name_of_file[:-5]]
    # print(name_of_file)
    with open('data/fight_json/'+name_of_file) as fight_data:    
        data = json.load(fight_data)
        fighters_names = get_fighters_name_from_fight_json(data) #(Blue,Red)
        fighters_id = get_fighters_id_from_fight_json(data)
        if fighters_id == "error":
            files_with_different_template.append(name_of_file)
            return None
        #check if fighter profile available before
        for index,fighter in enumerate(fighters_id):
            if fighter not in fighters_profiles.keys():
                foo = get_fighter_profile_template()
                fighters_profiles[fighter] = foo
                fighters_profiles[fighter]["Fighter"]["FighterID"] = fighter
                fighters_profiles[fighter]["Fighter"]["Name"] = fighters_names[index]
            with open('data/time_bound_profiles/'+name_of_file[:-5]+'_'+fighter+'.json', 'w') as outfile:
                json.dump(fighters_profiles[fighter], outfile,sort_keys=True, indent=4)
            # update_profile(data,fighters_id[i],i,winner_id)
                




fighters_profiles = {}
files_with_different_template = []

all_fights_json_names = get_name_of_all_fight_json()
all_fights_json_names.sort()
result_of_fights = get_all_results()

for file_name in all_fights_json_names:
    master_loop(file_name)

print(files_with_different_template[:5])