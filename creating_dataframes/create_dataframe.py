import os
import json
import pandas as pd
import pprint
import collections

listoffiles = os.listdir("./Data/Fights")

def flatten(d, parent_key='', sep='_'):
    print "in flatten"
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def create_dict(indict):
  return {
      'Event_ID': indict['FMLiveFeed']['EventID'],
      'Fight_ID': indict['FMLiveFeed']['FightID'],
      'Blue_Fighter_ID': indict['FMLiveFeed']['Fighters']['Blue']['FighterID'],
      'Blue_Name': indict['FMLiveFeed']['Fighters']['Blue']['Name'],
      'Red_Fighter_ID': indict['FMLiveFeed']['Fighters']['Red']['FighterID'],
      'Red_Name': indict['FMLiveFeed']['Fighters']['Red']['Name']
  }


def readfile(inputstr, header,flag=False):
  print "in readFile"
  with open(header + inputstr) as datafile:
    herp = json.load(datafile)
    if(flag):
      event_fight = inputstr.split('_')
      herp['Event_id'] = event_fight[0]
      herp['Fight_id'] = event_fight[1].split('.')[0]
      boobs = herp['Fighter']
    return herp


def EditDict(indict):
  print "in EditDict"
  bluefighterstring = str(indict['Event_ID'])+str('_')+str(indict['Fight_ID'])+str('_')+ str(indict['Blue_Fighter_ID'])+'.json'
  redfighterstring = str(indict['Event_ID'])+str('_')+str(indict['Fight_ID'])+str('_')+ str(indict['Red_Fighter_ID'])+'.json'
  blue_fighter_dict = readfile(bluefighterstring,'./Data/Fights_Fighter/')
  red_fighter_dict = readfile(redfighterstring,'./Data/Fights_Fighter/')
  val = blue_fighter_dict['Fighter_stats']
  blue_fighter_dict['Blue_Fighter_stats'] = val
  val = blue_fighter_dict['Record']
  blue_fighter_dict['BlueRecord'] = val
  blue_fighter_dict.pop('Fighter',None)
  blue_fighter_dict.pop('Fighter_stats',None)
  blue_fighter_dict.pop('Record',None)
  indict.update(blue_fighter_dict)
  val = red_fighter_dict['Fighter_stats']
  red_fighter_dict['Red_Fighter_stats'] = val
  val = red_fighter_dict['Record']
  red_fighter_dict['RedRecord'] = val
  red_fighter_dict.pop('Record',None)
  red_fighter_dict.pop('Fighter',None)
  red_fighter_dict.pop('Fighter_stats',None)
  indict.update(red_fighter_dict)
  if (winners[str(indict['Event_ID'])+'_'+str(indict['Fight_ID'])] == indict['Blue_Fighter_ID']):
    indict['winner'] = 'blue'
  elif (winners[str(indict['Event_ID'])+'_'+str(indict['Fight_ID'])] == indict['Red_Fighter_ID']):
    indict['winner'] = 'red'
  elif(winners[str(indict['Event_ID'])+'_'+str(indict['Fight_ID'])]== '11111'):
    indict['winner'] = 'draw'
  else:
    indict['winner'] = 'no contest'
  return indict

pp = pprint.PrettyPrinter(indent=2)

jsons = [readfile(x,"./Data/Fights/") for x in listoffiles]

FighterAndEventDic = map(create_dict, jsons)
# At this point I have a list of dict with Event ID, Fight ID 
# and both red and blue fighter IDs
# Now iterate through this dict and edit the members. 

winners = readfile("Fights_winner.json","./Data/")
updatedDicts = map(EditDict,FighterAndEventDic)
flatteneddicts = map(flatten,updatedDicts)
pp.pprint(flatteneddicts[-2])
df = pd.DataFrame.from_records(flatteneddicts)
df.to_csv('./Data/finalout.csv')
