import json
import datetime
from os import listdir
from os.path import isfile, join


fighters_profiles = {}
files_with_different_template = []
fighters_profiles_template = {}


def get_fighter_profile_template():
    with open('fighter_profile.json') as data_file:
        return json.load(data_file)

def get_all_results():
    with open('winners.json') as data_file:    
        return json.load(data_file)

def get_all_json():
    return [f for f in listdir("json/") if isfile(join("json/", f))]

def get_fighters_name_from_fight_json(data):
    try:
        return (data["FMLiveFeed"]["Fighters"]["Blue"]["Name"],data["FMLiveFeed"]["Fighters"]["Red"]["Name"])
    except KeyError: 
        return "error"

def get_fighters_id_from_fight_json(data):
    try:
        return (data["FMLiveFeed"]["Fighters"]["Blue"]["FighterID"],data["FMLiveFeed"]["Fighters"]["Red"]["FighterID"])
    except KeyError: 
        return "error"

def add_time_stamps(time1,time2):
    time1 =  datetime.datetime.strptime(time1, '%M:%S')
    time2 = datetime.datetime.strptime(time2, '%M:%S')
    return str(datetime.timedelta(minutes = time1.minute,seconds = time1.second)+datetime.timedelta(minutes = time2.minute,seconds = time2.second))#.strftime('%M:%S')

def get_formated_int_value(value):
    if value == "":
        return 0
    elif value[-1] == '*':
        return int(value[:-1])
    else:
        return int(value)

def update_profile(data,id,i):
    global fighters_profiles
    round_data_fight = data["FMLiveFeed"]["RoundStats"]
    round_data_fighter = fighters_profiles[id]["Fighter_stats"]
    for key in round_data_fight.keys():
        if i == 0:
            for style in round_data_fight[key]["Blue"].keys():
                if style == "Grappling" or style == "Strikes":
                    for move in round_data_fight[key]["Blue"][style].keys():
                        for value in round_data_fight[key]["Blue"][style][move].keys():
                            value_in_fight_data = round_data_fight[key]["Blue"][style][move][value]
                            value_in_fight_data = get_formated_int_value(value_in_fight_data)
                            value_in_fighter_profile = round_data_fighter[key][style][move][value]
                            value_in_fighter_profile = get_formated_int_value(value_in_fighter_profile)
                            value_in_fighter_profile+=value_in_fight_data
                            round_data_fighter[key][style][move][value] = str(value_in_fighter_profile)
        else:
            for style in round_data_fight[key]["Red"].keys():
                if style == "Grappling" or style == "Strikes":
                    for move in round_data_fight[key]["Red"][style].keys():
                        for value in round_data_fight[key]["Red"][style][move].keys():
                            value_in_fight_data = round_data_fight[key]["Red"][style][move][value]
                            value_in_fight_data = get_formated_int_value(value_in_fight_data)
                            value_in_fighter_profile = round_data_fighter[key][style][move][value]
                            value_in_fighter_profile = get_formated_int_value(value_in_fighter_profile)
                            value_in_fighter_profile+=value_in_fight_data
                            round_data_fighter[key][style][move][value] = str(value_in_fighter_profile)

def master_loop(name_of_file):
    # print name_of_file
    global fighters_profiles
    with open('json/'+name_of_file) as data_file:    
        data = json.load(data_file)
        fighters_names = get_fighters_name_from_fight_json(data) #(Blue,Red)
        fighters_id = get_fighters_id_from_fight_json(data)
        if fighters_id == "error":
            files_with_different_template.append(name_of_file)
            return 0
        #check if fighter profile available before
        for i in xrange(0,2):
            if fighters_id[i] not in fighters_profiles:
                fighters_profiles[fighters_id[i]] = fighters_profiles_template
                fighters_profiles[fighters_id[i]]["Fighter"]["FighterID"] = fighters_id[i]
                fighters_profiles[fighters_id[i]]["Fighter"]["Name"] = fighters_names[i]
            with open('profile_json/'+name_of_file[:-5]+'_'+fighters_id[i]+'.json', 'w') as outfile:
                json.dump(fighters_profiles[fighters_id[i]], outfile, indent=4)
            update_profile(data,fighters_id[i],i)
                


def main():
    all_fights_json_names = get_all_json()
    all_fights_json_names.sort()
    result_of_fights = get_all_results()
    global fighters_profiles_template
    fighters_profiles_template = get_fighter_profile_template()
    for file_name in all_fights_json_names:
        master_loop(file_name)

    # for f in foo:
    #     print f 
    # print len(foo)


main()

# with open('json/646_4580.json') as data_file:    
#     data = json.load(data_file)
#     fighters_names = get_fighters_name_from_fight_json(data) #(Blue,Red)
#     fighters_id = get_fighters_id_from_fight_json(data)
#     round_stats = data["FMLiveFeed"]["RoundStats"]
#     keys_in_round_stats = round_stats.keys()
#     print keys_in_round_stats
    # print fighters_names 
    # print add_time_stamps(data["FMLiveFeed"]["RoundStats"]["Round2"]["Blue"]["TIP"]["Guard Control Time"],data["FMLiveFeed"]["RoundStats"]["Round2"]["Blue"]["TIP"]["Guard Control Time"])
    # print  int(data["FMLiveFeed"]["RoundStats"]["Round2"]["Blue"]["Strikes"]["Ground Significant Punches"]["Landed"][:-1])

