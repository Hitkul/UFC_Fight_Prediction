import requests
from bs4 import BeautifulSoup
import json
from urllib.request import urlopen

fight_id = []
event_id = 0

fight_json_dump_location = "fight_json"

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
		start_year+=1;
	return links

def get_json():
	print("in get_json")
	for h in fight_id:
		print((h+"    "+str(event_id)))
		url = "http://liveapi.fightmetric.com/V2/"+str(event_id)+"/"+str(h)+"/Stats.json"
		# print url
		print(url)
		data = json.load(urlopen(url))
		print("got json")
		# print h
		with open('json/'+str(event_id)+"_"+str(h)+'.json', 'w') as outfile:
	    		json.dump(data, outfile,indent=4)	
	print("leaving get_json")


def get_event_and_fight_ids(link):
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
		print(fight_id)
		source = plain_text.decode("utf-8")
		edit  = source[source.find("document.refreshURL =")+57:source.find("document.refreshURL =")+60]
		global event_id
		event_id = edit
		return event_id,fight_id


past_event_links = get_link_of_past_events(2014,2018)
for link in past_event_links:
	event_id,fight_id = get_event_and_fight_ids(link)



