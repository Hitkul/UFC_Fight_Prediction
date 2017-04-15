import json
import datetime


def get_fighters_name_from_fight_json(data):
	return (data["FMLiveFeed"]["Fighters"]["Blue"]["Name"],data["FMLiveFeed"]["Fighters"]["Red"]["Name"])

def get_fighters_id_from_fight_json(data):
	return (data["FMLiveFeed"]["Fighters"]["Blue"]["FighterID"],data["FMLiveFeed"]["Fighters"]["Red"]["FighterID"])

def add_time_stamps(time1,time2):
    time1 =  datetime.datetime.strptime(time1, '%M:%S')
    time2 = datetime.datetime.strptime(time2, '%M:%S')
    return str(datetime.timedelta(minutes = time1.minute,seconds = time1.second)+datetime.timedelta(minutes = time2.minute,seconds = time2.second))#.strftime('%M:%S')

with open('json/646_4580.json') as data_file:    
    data = json.load(data_file)
    fighters_names = get_fighters_name_from_fight_json(data) #(Blue,Red)
    fighters_id = get_fighters_id_from_fight_json(data)
    round_stats = data["FMLiveFeed"]["RoundStats"]
    keys_in_round_stats = round_stats.keys()
    print keys_in_round_stats
    # print fighters_names 
    # print add_time_stamps(data["FMLiveFeed"]["RoundStats"]["Round2"]["Blue"]["TIP"]["Guard Control Time"],data["FMLiveFeed"]["RoundStats"]["Round2"]["Blue"]["TIP"]["Guard Control Time"])
    # print  int(data["FMLiveFeed"]["RoundStats"]["Round2"]["Blue"]["Strikes"]["Ground Significant Punches"]["Landed"][:-1])