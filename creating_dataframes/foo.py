import os
import json
import pandas as pd
import pprint
import collections

listoffiles = os.listdir("./Data/Fights")
def flatten(d, parent_key='', sep='_'):
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
      'Blue_fighter_id': indict['FMLiveFeed']['Fighters']['Blue']['FighterID'],
      'Blue_name': indict['FMLiveFeed']['Fighters']['Blue']['Name'],
      'Red_fighter_id': indict['FMLiveFeed']['Fighters']['Red']['FighterID'],
      'Red_name': indict['FMLiveFeed']['Fighters']['Red']['Name']
  }
def readfile(inputstr, header):
  global count
  count +=1
  print count
  with open(header + inputstr) as datafile:
    return json.load(datafile)

pp = pprint.PrettyPrinter(indent=2)
count = 0
jsons = [readfile(x,"./Data/Fights/") for x in listoffiles]
FighterAndEventDict = map(create_dict, jsons)
count = 0
listoffiles = os.listdir("./Data/Fights_Fighter")
jsons = [readfile(x,"./Data/Fights_Fighter/") for x in listoffiles]
flattenedjsons = [flatten(x) for x in jsons]
pp.pprint(flattenedjsons[0]) 



df = pd.DataFrame.from_records(FighterAndEventDict)
print df.head()
