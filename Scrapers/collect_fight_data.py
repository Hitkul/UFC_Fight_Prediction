import requests
from bs4 import BeautifulSoup
import json
from urllib.request import urlopen


fight_json_dump_location = "data/fight_json"
fights_failed_to_fetch = []
winners_failed_to_fetch = []
methods_failed_to_fetch = []
results_record = dict()

def get_link_of_past_events(start_year,end_year):
	links = []
	while start_year <= end_year:
		url = 'http://www.ufc.com/event/Past_Events?year='+str(start_year)
		source_code = requests.get(url, allow_redirects=False)
		# print(source_code.raw)
		plain_text = source_code.text.encode('ascii', 'replace')
		soup = BeautifulSoup(plain_text,'html.parser')
		for link in soup.findAll('td',{'class': 'event-title'}):
			for href in link.findAll('a'):
				foo = href.get('href')
				links.append(foo)
		start_year+=1
	return links

def get_fight_json(event_id,fight_id):
	print(f"fetching {event_id} - {fight_id}")
	try:
		url = "http://liveapi.fightmetric.com/V2/"+str(event_id)+"/"+str(fight_id)+"/Stats.json"
		return json.load(urlopen(url))
	except:
		print("error occured while fetching")
		global fights_failed_to_fetch
		fights_failed_to_fetch.append((event_id,fight_id))
		return None


def get_fight_winner(event_id):
	print(f"fetching winners of fight {event_id}")
	global results_record
	url = "http://m.ufc.com/fm/api/event/detail/"+str(event_id)+".json"
	try:
		data = json.load(urlopen(url))
		json_for_each_fight = data["FightCard"]
	except:
		print("could not fetch result for this")
		global winners_failed_to_fetch
		winners_failed_to_fetch.append(event_id)
	
	for fight in json_for_each_fight:
		fight_id = fight["statid"]
		json_for_each_fighter = fight["Fighters"]
		for fighter in json_for_each_fighter:
			if fighter["Outcome"]["OutcomeID"] == "1"  :
				winning_fighter_id = fighter["statid"]
				results_record[str(event_id)+"_"+str(fight_id)] = winning_fighter_id
				break
			elif fighter["Outcome"]["OutcomeID"] == "4":
				results_record[str(event_id)+"_"+str(fight_id)] = "00000"# no contest
				break
			elif fighter["Outcome"]["OutcomeID"] == "3":
				results_record[str(event_id)+"_"+str(fight_id)] = "11111"#draw
				break

def get_win_method(event_id):
	print(f"fetching win method of fight {event_id}")	
	global results_record
	url = "http://liveapi.fightmetric.com/V1/"+str(event_id)+"/Fnt.json"
	try:
		data = json.load(urlopen(url))
	except:
		print("failed to fetch win method")
		global methods_failed_to_fetch
		methods_failed_to_fetch.append(event_id)
		for key in results_record.keys():
			if key.split("_")[0] == str(event_id):
				results_record[key] = [results_record[key],None]	
		return None
	json_for_each_fight = data["FMLiveFeed"]["Fights"]
	for fight in json_for_each_fight:
		method = fight["Method"]
		fight_id = fight["FightID"]
		key = str(event_id)+"_"+fight_id
		if key in results_record.keys():
			results_record[key] = [results_record[key],method] 
		else:
			results_record[key] = [None,method] 

def dump_json(data,location):
	with open(location+'.json', 'w') as outfile:
		json.dump(data, outfile,indent=4)	



def get_event_and_fight_ids(link):
	print("getting event_id and fight_ids")
	url = 'http://www.ufc.com'+link
	source_code = requests.get(url, allow_redirects=False)
	plain_text = source_code.text.encode('ascii', 'replace')
	source = plain_text.decode("utf-8")
	edit  = source[source.find("fightOutcomeData"):]
	foo = edit.split(";")
	bar = foo[0][foo[0].find("{"):]
	bar = bar[1:-1]
	sheep = bar.split(",")
	fight_id=[]
	for h in sheep:
		fight_id.append(h[:h.find(":")][1:-1])
	source = plain_text.decode("utf-8")
	edit  = source[source.find("document.refreshURL =")+57:source.find("document.refreshURL =")+60]
	global event_id
	event_id = edit
	return event_id,fight_id


past_event_links = get_link_of_past_events(2014,2014)

for link in past_event_links:
	event_id,fight_id = get_event_and_fight_ids(link)
	
	for fight in fight_id:
		data = get_fight_json(event_id,fight)
		if data!=None:
			dump_json(data,fight_json_dump_location+"/"+str(event_id)+'_'+str(fight))

	get_fight_winner(event_id)

	get_win_method(event_id)

	dump_json(results_record,"data/results_record")

with open('failed_history/fights_failed_to_fetch.txt', 'w') as f:
    for item in fights_failed_to_fetch:
        f.write("%s\n" % item)


with open('failed_history/winners_failed_to_fetch.txt', 'w') as f:
    for item in winners_failed_to_fetch:
        f.write("%s\n" % item)


with open('failed_history/methods_failed_to_fetch.txt', 'w') as f:
    for item in methods_failed_to_fetch:
        f.write("%s\n" % item)





