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

def update_profile(data):
    pass

def master_loop(name_of_file):
    # print name_of_file
    global fighter_profile
    with open('json/'+name_of_file) as data_file:    
        data = json.load(data_file)
        fighters_names = get_fighters_name_from_fight_json(data) #(Blue,Red)
        fighters_id = get_fighters_id_from_fight_json(data)
        if fighters_id == "error":
            files_with_different_template.append(name_of_file)
            return 0
        #check if fighter profile available before
        for id in fighters_id:
            if id not in fighters_profiles:
                fighters_profiles[id] = fighters_profiles_template
            with open('profile_json/'+name_of_file[:-5]+'_'+id+'.json', 'w') as outfile:
                json.dump(fighters_profiles[id], outfile, indent=4)
            update_profile(data)
                


def main():
    all_fights_json_names = get_all_json()
    all_fights_json_names.sort()
    result_of_fights = get_all_results()
    global fighters_profiles_template
    fighters_profiles_template = get_fighter_profile_template()
    # print fighters_profiles_template
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

